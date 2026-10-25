#!/usr/bin/env python3
"""Build reproducible inventories for the original thesis PDF.

The output is an audit aid, not a substitute for reading the PDF. Citation
candidates are deliberately preserved with page and context for manual review.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source" / "Étude_bibliographique_sur_les_fondations_de_ponts.pdf"
OUT = ROOT / "audits"
OUT.mkdir(parents=True, exist_ok=True)


def norm_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def slug_key(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


doc = pymupdf.open(SOURCE)
pages = [page.get_text("text", sort=True) for page in doc]
source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()

# Full text with explicit PDF page boundaries.
with (OUT / "original_text_by_page.txt").open("w", encoding="utf-8") as f:
    for number, text in enumerate(pages, 1):
        f.write(f"\n===== PDF PAGE {number} =====\n{text}")

# Page inventory and text JSONL for later targeted audits.
with (OUT / "pages.jsonl").open("w", encoding="utf-8") as f:
    for number, (page, text) in enumerate(zip(doc, pages), 1):
        record = {
            "pdf_page": number,
            "characters": len(text),
            "words": len(re.findall(r"\b\w+\b", text, re.UNICODE)),
            "embedded_images": len(page.get_images(full=True)),
            "drawings": len(page.get_drawings()),
            "text": text,
        }
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

# Headings and captions, with a line-level excerpt to ease manual verification.
heading_re = re.compile(
    r"^\s*((?:CHAPITRE\s+[IVX]+)|(?:[IVX]+\.\d+(?:\.\d+)*)\s+.+|"
    r"(?:INTRODUCTION|CONCLUSION|BIBLIOGRAPHIE|RÉSUMÉ|ABSTRACT|ملخص).*)$",
    re.IGNORECASE,
)
caption_re = re.compile(r"^\s*((?:Figure|Tableau)\s+([IVX]+\.\d+)\s*:?\s*(.*))$", re.IGNORECASE)
index_rows: list[dict[str, object]] = []
for number, text in enumerate(pages, 1):
    for line in text.splitlines():
        stripped = norm_space(line)
        if not stripped:
            continue
        h = heading_re.match(line)
        if h and len(stripped) < 240:
            index_rows.append({"type": "heading", "label": "", "page": number, "text": stripped})
            continue
        c = caption_re.match(line)
        if c:
            index_rows.append({"type": "caption", "label": c.group(2), "page": number, "text": stripped})

with (OUT / "document_index.csv").open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["type", "label", "page", "text"])
    writer.writeheader()
    writer.writerows(index_rows)

# Bibliography: in the supplied PDF each entry begins at the left margin and
# continuation lines are indented. This convention is checked in the report.
bibliography: list[dict[str, object]] = []
for number in range(195, 199):
    current: dict[str, object] | None = None
    for raw in pages[number - 1].splitlines():
        if not raw.strip() or re.fullmatch(r"\s*\d+\s*", raw):
            continue
        starts_entry = raw == raw.lstrip()
        if starts_entry:
            if current:
                bibliography.append(current)
            current = {"id": len(bibliography) + 1, "start_pdf_page": number, "parts": [raw.strip()]}
        elif current:
            current["parts"].append(raw.strip())
    if current:
        bibliography.append(current)

for entry in bibliography:
    entry["text"] = norm_space(" ".join(entry.pop("parts")))
    match = re.match(r"(.+?)\s*\(((?:19|20)\d{2}[a-z]?)\)", str(entry["text"]))
    entry["authors_raw"] = match.group(1).strip() if match else ""
    entry["year"] = match.group(2) if match else ""
    first_author = re.split(r"\s*(?:,|\bet\b|&)\s*", str(entry["authors_raw"]), maxsplit=1)[0]
    entry["first_author_key"] = slug_key(first_author)

with (OUT / "bibliography_entries.json").open("w", encoding="utf-8") as f:
    json.dump(bibliography, f, ensure_ascii=False, indent=2)
with (OUT / "bibliography_entries.csv").open("w", encoding="utf-8", newline="") as f:
    fields = ["id", "start_pdf_page", "authors_raw", "year", "first_author_key", "text"]
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows({k: entry.get(k, "") for k in fields} for entry in bibliography)

# Citation candidates in the body. Both parenthetical and narrative forms are
# retained; duplicates and false positives are resolved during manual review.
paren_re = re.compile(r"\(([^()]{0,180}?(?:19|20)\d{2}[a-z]?[^()]{0,100}?)\)")
narrative_re = re.compile(
    r"(?<![\w-])([A-ZÀ-Þ][A-ZÀ-Þ0-9'’.,&;\- ]{1,100}?)\s*"
    r"\(((?:19|20)\d{2}[a-z]?(?:\s*[,;]\s*(?:19|20)\d{2}[a-z]?)*)\)"
)
contexts: list[dict[str, object]] = []
for number, text in enumerate(pages[:194], 1):
    flat = norm_space(text)
    seen_spans: set[tuple[int, int]] = set()
    for kind, regex in (("parenthetical", paren_re), ("narrative", narrative_re)):
        for match in regex.finditer(flat):
            span = match.span()
            if kind == "narrative" and any(a <= span[0] and span[1] <= b for a, b in seen_spans):
                continue
            if kind == "parenthetical":
                seen_spans.add(span)
            raw = match.group(0)
            context = flat[max(0, span[0] - 100) : min(len(flat), span[1] + 120)]
            contexts.append({"pdf_page": number, "kind": kind, "raw": raw, "context": context})

with (OUT / "citation_contexts.csv").open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["pdf_page", "kind", "raw", "context"])
    writer.writeheader()
    writer.writerows(contexts)

# Group by the exact candidate string and provide pages/count. This is an
# inventory of candidates, not a claim that every candidate is a valid citation.
groups: dict[str, dict[str, object]] = {}
for item in contexts:
    raw = str(item["raw"])
    group = groups.setdefault(raw, {"raw": raw, "count": 0, "pages": set()})
    group["count"] = int(group["count"]) + 1
    group["pages"].add(item["pdf_page"])
with (OUT / "citation_candidates_grouped.csv").open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["raw", "count", "pages"])
    writer.writeheader()
    for group in sorted(groups.values(), key=lambda g: slug_key(str(g["raw"]))):
        writer.writerow({"raw": group["raw"], "count": group["count"], "pages": ";".join(map(str, sorted(group["pages"])))})

summary = {
    "source": str(SOURCE.relative_to(ROOT)),
    "source_sha256": source_hash,
    "pdf_pages": len(doc),
    "body_pages_scanned_for_citation_candidates": 194,
    "bibliography_pages_scanned": [195, 196, 197, 198],
    "bibliography_entry_count_by_hanging_indent": len(bibliography),
    "bibliography_entries_without_detected_author_year": [e["id"] for e in bibliography if not e["year"]],
    "document_index_rows": len(index_rows),
    "citation_candidate_occurrences": len(contexts),
    "citation_candidate_distinct_strings": len(groups),
    "total_words_by_extraction": sum(len(re.findall(r"\b\w+\b", text, re.UNICODE)) for text in pages),
    "notes": [
        "Counts are derived from the supplied PDF and must be visually checked for layout exceptions.",
        "Citation candidates require manual normalization; regex matches are not automatically valid references.",
        "The bibliography count uses the visible hanging-indent convention on PDF pages 195-198.",
    ],
}
(OUT / "audit_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False, indent=2))
