import re
import json
import pickle
from pathlib import Path
from typing import List, Dict, Any, Optional
from rank_bm25 import BM25Okapi
from app.parser import DocumentParser
from app.manifest import ManifestRegistry, ManifestEntry

class DocumentChunk:
    def __init__(
        self,
        chunk_id: str,
        doc_path: str,
        doc_title: str,
        section_title: str,
        text: str,
        audience: str,
        status: str,
        last_updated: str,
        authority: int,
        superseded_by: Optional[str] = None
    ):
        self.chunk_id = chunk_id
        self.doc_path = doc_path
        self.doc_title = doc_title
        self.section_title = section_title
        self.text = text
        self.audience = audience
        self.status = status
        self.last_updated = last_updated
        self.authority = authority
        self.superseded_by = superseded_by

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chunk_id": self.chunk_id,
            "doc_path": self.doc_path,
            "doc_title": self.doc_title,
            "section_title": self.section_title,
            "text": self.text,
            "audience": self.audience,
            "status": self.status,
            "last_updated": self.last_updated,
            "authority": self.authority,
            "superseded_by": self.superseded_by
        }

class CorpusIndex:
    def __init__(self):
        self.chunks: List[DocumentChunk] = []
        self.raw_documents: Dict[str, str] = {}
        self.bm25: Optional[BM25Okapi] = None
        self.tokenized_corpus: List[List[str]] = []
        self.manifest_registry: Optional[ManifestRegistry] = None

    @staticmethod
    def tokenize(text: str) -> List[str]:
        # Lowercase, clean alphanumeric tokens
        tokens = re.findall(r"\b[a-zA-Z0-9_\-\.]+\b", text.lower())
        return tokens

    def build_from_corpus(self, corpus_dir: Path, manifest_path: Optional[Path] = None):
        if not manifest_path:
            manifest_path = corpus_dir / "_manifest.csv"
        
        self.manifest_registry = ManifestRegistry(manifest_path)
        self.chunks = []
        self.raw_documents = {}

        manifest_entries = self.manifest_registry.entries

        for rel_path, entry in manifest_entries.items():
            file_path = corpus_dir / rel_path
            if not file_path.exists():
                # try alternative separator
                file_path = corpus_dir / rel_path.replace("/", "\\")
            if not file_path.exists():
                continue

            raw_text = DocumentParser.parse_file(file_path)
            if not raw_text.strip():
                continue

            self.raw_documents[rel_path] = raw_text

            # Semantic chunking by markdown headers or paragraph blocks
            paragraphs = re.split(r"\n\s*\n", raw_text)
            current_section = entry.title
            accumulated_text = []
            chunk_num = 0

            for para in paragraphs:
                para = para.strip()
                if not para:
                    continue

                if para.startswith("#"):
                    current_section = para.lstrip("#").strip().split("\n")[0]

                accumulated_text.append(para)
                combined = "\n\n".join(accumulated_text)

                # Keep chunks around 100-350 words
                if len(combined.split()) >= 120 or para == paragraphs[-1]:
                    chunk_id = f"{rel_path}#{chunk_num}"
                    chunk_num += 1
                    chunk = DocumentChunk(
                        chunk_id=chunk_id,
                        doc_path=rel_path,
                        doc_title=entry.title,
                        section_title=current_section,
                        text=combined,
                        audience=entry.audience,
                        status=entry.status,
                        last_updated=entry.last_updated,
                        authority=entry.authority,
                        superseded_by=self.manifest_registry.superseded_by.get(rel_path)
                    )
                    self.chunks.append(chunk)
                    accumulated_text = []

        # Build BM25 index
        self.tokenized_corpus = [self.tokenize(c.text + " " + c.doc_title + " " + c.section_title) for c in self.chunks]
        self.bm25 = BM25Okapi(self.tokenized_corpus)

    def save(self, cache_dir: Path):
        cache_dir.mkdir(parents=True, exist_ok=True)
        data = {
            "chunks": [c.to_dict() for c in self.chunks],
            "raw_documents": self.raw_documents
        }
        with open(cache_dir / "index_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        with open(cache_dir / "bm25.pkl", "wb") as f:
            pickle.dump({"bm25": self.bm25, "tokenized": self.tokenized_corpus}, f)

    @classmethod
    def load(cls, cache_dir: Path, manifest_path: Path) -> "CorpusIndex":
        idx = cls()
        idx.manifest_registry = ManifestRegistry(manifest_path)
        with open(cache_dir / "index_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        idx.raw_documents = data["raw_documents"]
        idx.chunks = [
            DocumentChunk(**d) for d in data["chunks"]
        ]
        with open(cache_dir / "bm25.pkl", "rb") as f:
            bm25_data = pickle.load(f)
            idx.bm25 = bm25_data["bm25"]
            idx.tokenized_corpus = bm25_data["tokenized"]
        return idx
