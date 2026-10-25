#!/usr/bin/env python3
"""Inventory extracted reference PDFs without modifying them.

Outputs a traceable CSV/JSON summary in the repository and a larger opening-text
search index outside Git. The inventory records facts only; relevance and source
quality require a separate manual review.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import pymupdf


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def clean(value: object, limit: int = 1000) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    return text[:limit]


def inspect_pdf(path: Path) -> dict[str, object]:
    result: dict[str, object] = {
        "pages": "",
        "pdf_title": "",
        "pdf_author": "",
        "parse_status": "not_attempted",
        "opening_text": "",
    }
    try:
        with pymupdf.open(path) as document:
            result["pages"] = document.page_count
            result["pdf_title"] = clean(document.metadata.get("title"), 500)
            result["pdf_author"] = clean(document.metadata.get("author"), 300)
            result["parse_status"] = "ok" if document.page_count else "empty_pdf"
            if document.page_count:
                result["opening_text"] = clean(document[0].get_text("text"), 3000)
            if document.is_encrypted:
                result["parse_status"] = "encrypted_readable"
    except Exception as exc:  # Keep one corrupt file from stopping the inventory.
        result["parse_status"] = f"error: {type(exc).__name__}: {clean(exc, 250)}"
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("library", type=Path)
    parser.add_argument("output_directory", type=Path)
    parser.add_argument("--search-index", type=Path)
    args = parser.parse_args()
    library = args.library.resolve()
    output = args.output_directory.resolve()
    output.mkdir(parents=True, exist_ok=True)
    paths = sorted(
        (p for p in library.rglob("*") if p.is_file() and p.suffix.lower() == ".pdf"),
        key=lambda p: p.relative_to(library).as_posix().casefold(),
    )
    rows: list[dict[str, object]] = []
    search_stream = args.search_index.open("w", encoding="utf-8") if args.search_index else None
    try:
        for index, path in enumerate(paths, 1):
            relative = path.relative_to(library).as_posix()
            stat = path.stat()
            details = inspect_pdf(path)
            opening_text = details.pop("opening_text")
            row = {
                "reference_id": f"PDF{index:04d}",
                "relative_path": relative,
                "category": relative.split("/", 1)[0] if "/" in relative else "racine",
                "bytes": stat.st_size,
                "sha256": sha256_file(path),
                **details,
            }
            rows.append(row)
            if search_stream:
                search_stream.write(json.dumps({
                    "reference_id": row["reference_id"],
                    "relative_path": relative,
                    "sha256": row["sha256"],
                    "opening_text": opening_text,
                }, ensure_ascii=False) + "\n")
            if index % 100 == 0 or index == len(paths):
                print(f"INSPECTED {index}/{len(paths)}", flush=True)
    finally:
        if search_stream:
            search_stream.close()

    groups: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        groups[str(row["sha256"])].append(str(row["reference_id"]))
    duplicate_group = 0
    for members in groups.values():
        if len(members) > 1:
            duplicate_group += 1
            label = f"DUP{duplicate_group:04d}"
            for member in members:
                rows[int(member[3:]) - 1]["duplicate_group"] = label
    for row in rows:
        row.setdefault("duplicate_group", "")

    fields = [
        "reference_id", "relative_path", "category", "bytes", "sha256", "pages",
        "pdf_title", "pdf_author", "parse_status", "duplicate_group",
    ]
    csv_path = output / "archive_pdf_inventory.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    status_counts = Counter(str(row["parse_status"]).split(":", 1)[0] for row in rows)
    summary = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "library": str(library),
        "pdf_count": len(rows),
        "pdf_bytes": sum(int(row["bytes"]) for row in rows),
        "pdf_pages_when_readable": sum(int(row["pages"]) for row in rows if str(row["pages"]).isdigit()),
        "unique_sha256": len(groups),
        "duplicate_groups": sum(len(members) > 1 for members in groups.values()),
        "duplicate_file_instances_beyond_first": sum(len(members) - 1 for members in groups.values() if len(members) > 1),
        "parse_status_counts": dict(status_counts),
        "categories": dict(Counter(str(row["category"]) for row in rows)),
        "csv": str(csv_path),
        "search_index": str(args.search_index) if args.search_index else "",
        "note": "Inventory facts are not relevance or quality judgments; exact duplicates are not automatic deletion decisions.",
    }
    (output / "archive_inventory_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
