import argparse
import sys
from pathlib import Path
from app.indexer import CorpusIndex
from app.config import INDEX_CACHE_DIR

def main():
    parser = argparse.ArgumentParser(description="Rebuild Ferrowave answer engine index from corpus")
    parser.add_argument("--corpus", type=str, default="corpus", help="Path to corpus directory")
    parser.add_argument("--manifest", type=str, default=None, help="Optional path to _manifest.csv")
    args = parser.parse_args()

    corpus_dir = Path(args.corpus)
    if not corpus_dir.exists():
        print(f"Error: Corpus directory {corpus_dir} does not exist.", file=sys.stderr)
        sys.exit(1)

    manifest_path = Path(args.manifest) if args.manifest else corpus_dir / "_manifest.csv"
    print(f"Building index from: {corpus_dir} (manifest: {manifest_path})")
    
    idx = CorpusIndex()
    idx.build_from_corpus(corpus_dir, manifest_path)
    idx.save(INDEX_CACHE_DIR)
    
    print(f"Index successfully rebuilt and saved to {INDEX_CACHE_DIR}.")
    print(f"Total documents indexed: {len(idx.raw_documents)}")
    print(f"Total chunks created: {len(idx.chunks)}")

if __name__ == "__main__":
    main()
