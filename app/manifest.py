import csv
from pathlib import Path
from typing import Dict, Optional
from pydantic import BaseModel

class ManifestEntry(BaseModel):
    path: str
    title: str
    audience: str  # public | internal
    status: str    # current | superseded | draft
    last_updated: str
    supersedes: Optional[str] = None
    notes: Optional[str] = None
    authority: int = 50

class ManifestRegistry:
    def __init__(self, manifest_path: Path):
        self.entries: Dict[str, ManifestEntry] = {}
        self.superseded_by: Dict[str, str] = {}
        if manifest_path.exists():
            self._load(manifest_path)

    def _load(self, manifest_path: Path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                norm_path = row["path"].replace("\\", "/").strip()
                supersedes = row["supersedes"].replace("\\", "/").strip() if row.get("supersedes") else None
                
                # Assign authority weights based on policy and source hierarchy
                authority = 50
                if "policies/refund-policy.md" in norm_path or "legal/terms-of-service.pdf" in norm_path:
                    authority = 100
                elif norm_path.startswith("policies/"):
                    authority = 90
                elif norm_path.startswith("legal/"):
                    authority = 85
                elif norm_path.startswith("pricing/"):
                    authority = 80
                elif norm_path.startswith("product-docs/"):
                    authority = 70
                elif norm_path.startswith("release-notes/"):
                    authority = 60
                elif norm_path.startswith("support/"):
                    authority = 50
                elif norm_path.startswith("blog/"):
                    authority = 40
                elif norm_path.startswith("community/"):
                    authority = 20

                entry = ManifestEntry(
                    path=norm_path,
                    title=row.get("title", ""),
                    audience=row.get("audience", "public").strip(),
                    status=row.get("status", "current").strip(),
                    last_updated=row.get("last_updated", "").strip(),
                    supersedes=supersedes if supersedes else None,
                    notes=row.get("notes", ""),
                    authority=authority
                )
                self.entries[norm_path] = entry
                if supersedes:
                    self.superseded_by[supersedes] = norm_path

    def is_customer_accessible(self, path: str) -> bool:
        norm = path.replace("\\", "/").strip()
        entry = self.entries.get(norm)
        if not entry:
            # If not in manifest, be conservative if it says internal
            if "internal/" in norm or "draft" in norm.lower():
                return False
            return True
        # Exclude internal documents and drafts
        if entry.audience.lower() == "internal":
            return False
        if entry.status.lower() == "draft":
            return False
        return True

    def get_entry(self, path: str) -> Optional[ManifestEntry]:
        norm = path.replace("\\", "/").strip()
        return self.entries.get(norm)
