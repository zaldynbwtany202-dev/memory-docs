#!/usr/bin/env python3
"""Create a conservative author-year citation/bibliography crosswalk.

Only explicit author-year forms are normalized here. Bare years, dates of events,
and magnitude annotations are excluded. Every row retains page and context so a
human can resolve aliases and false positives instead of trusting a score.
"""
from __future__ import annotations

import csv
import difflib
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "audits"
pages = [json.loads(line) for line in (OUT / "pages.jsonl").read_text(encoding="utf-8").splitlines()]
bibliography = json.loads((OUT / "bibliography_entries.json").read_text(encoding="utf-8"))


def flat(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def key(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def first_author(authors: str) -> str:
    authors = authors.strip(" .;:")
    authors = re.split(r"\s+et\s+al\.?", authors, maxsplit=1, flags=re.I)[0]
    authors = re.split(r"\s+(?:et|and|&)\s+", authors, maxsplit=1, flags=re.I)[0]
    authors = authors.split(",", 1)[0]
    return authors.strip(" .;:")


YEAR = r"(?:19|20)\d{2}[a-z]?"
NAME = r"[A-ZÀ-Þ][A-ZÀ-Þ'’\-]+(?:\s+[A-Z]\.)?"
AUTHORS = NAME + r"(?:\s*,\s*" + NAME + r")*(?:\s+(?:et|and|&)\s+(?:al\.|" + NAME + r"))*"
narrative = re.compile(r"(?<![\w-])(" + AUTHORS + r")\s*\((" + YEAR + r"(?:\s*[,;]\s*" + YEAR + r")*)\)")
parenthetical = re.compile(r"\(([^()]{2,220}?" + YEAR + r"[^()]{0,120}?)\)")

records: list[dict[str, object]] = []
for page in pages[:194]:
    number = page["pdf_page"]
    text = flat(page["text"])
    for match in narrative.finditer(text):
        authors = match.group(1).strip()
        years = re.findall(YEAR, match.group(2))
        for year in years:
            records.append({
                "pdf_page": number,
                "form": "narrative",
                "authors_raw": authors,
                "year": year,
                "raw": match.group(0),
                "context": text[max(0, match.start() - 100): min(len(text), match.end() + 120)],
            })
    for match in parenthetical.finditer(text):
        content = match.group(1).strip()
        # A bibliographic parenthetical must contain an author/organization and
        # a comma immediately before at least one year. This excludes (1999),
        # earthquake dates, and magnitude annotations.
        if not re.search(r"[A-Za-zÀ-Þ][^;]*,\s*" + YEAR, content):
            continue
        for segment in re.split(r"\s*;\s*", content):
            year_match = re.search(r",\s*(" + YEAR + r")\s*$", segment.strip())
            if not year_match:
                continue
            authors = segment[:year_match.start()].strip(" ,;")
            if not authors or not re.search(r"[A-Za-zÀ-Þ]", authors):
                continue
            records.append({
                "pdf_page": number,
                "form": "parenthetical",
                "authors_raw": authors,
                "year": year_match.group(1),
                "raw": match.group(0),
                "context": text[max(0, match.start() - 100): min(len(text), match.end() + 120)],
            })

# Consolidate occurrences of one normalized author/year/raw form while keeping
# a representative context and every page.
groups: dict[tuple[str, str, str, str], dict[str, object]] = {}
for record in records:
    authors = str(record["authors_raw"])
    first = first_author(authors)
    group_key = (key(first), str(record["year"]), key(authors), str(record["form"]))
    group = groups.setdefault(group_key, {
        "first_author": first,
        "first_author_key": key(first),
        "authors_raw": authors,
        "year": record["year"],
        "form": record["form"],
        "count": 0,
        "pages": set(),
        "examples": [],
    })
    group["count"] = int(group["count"]) + 1
    group["pages"].add(record["pdf_page"])
    if len(group["examples"]) < 3:
        group["examples"].append({"page": number if (number := record["pdf_page"]) else record["pdf_page"], "raw": record["raw"], "context": record["context"]})

bib_by_key: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
for entry in bibliography:
    bib_by_key[(str(entry["first_author_key"]), str(entry["year"]))].append(entry)
all_bib_first_authors = sorted({str(e["first_author_key"]) for e in bibliography})

rows: list[dict[str, object]] = []
matched_bib_ids: set[int] = set()
for group in sorted(groups.values(), key=lambda g: (g["first_author_key"], g["year"], g["authors_raw"], g["form"])):
    matches = bib_by_key.get((group["first_author_key"], str(group["year"])), [])
    for match in matches:
        matched_bib_ids.add(int(match["id"]))
    nearest = difflib.get_close_matches(str(group["first_author_key"]), all_bib_first_authors, n=1, cutoff=0.72)
    rows.append({
        "first_author": group["first_author"],
        "authors_raw": group["authors_raw"],
        "year": group["year"],
        "form": group["form"],
        "occurrences": group["count"],
        "pages": ";".join(map(str, sorted(group["pages"]))),
        "match_status": "exact_first_author_year" if matches else "review_no_exact_match",
        "bibliography_ids": ";".join(str(m["id"]) for m in matches),
        "nearest_bibliography_author_for_review": nearest[0] if nearest else "",
        "example_raw": group["examples"][0]["raw"],
        "example_context": group["examples"][0]["context"],
    })

fields = ["first_author", "authors_raw", "year", "form", "occurrences", "pages", "match_status", "bibliography_ids", "nearest_bibliography_author_for_review", "example_raw", "example_context"]
with (OUT / "citation_bibliography_crosswalk.csv").open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)

unused = []
for entry in bibliography:
    if int(entry["id"]) not in matched_bib_ids:
        unused.append({"bibliography_id": entry["id"], "authors_raw": entry["authors_raw"], "year": entry["year"], "text": entry["text"], "review_status": "no_exact_normalized_citation_found__manual_review_required"})
with (OUT / "bibliography_not_matched_to_citations.csv").open("w", encoding="utf-8", newline="") as f:
    fields2 = ["bibliography_id", "authors_raw", "year", "review_status", "text"]
    writer = csv.DictWriter(f, fieldnames=fields2)
    writer.writeheader()
    writer.writerows(unused)

summary = {
    "normalized_citation_occurrences": len(records),
    "normalized_citation_groups": len(rows),
    "groups_with_exact_first_author_year_match": sum(r["match_status"] == "exact_first_author_year" for r in rows),
    "groups_requiring_review": sum(r["match_status"] != "exact_first_author_year" for r in rows),
    "bibliography_entries_matched_at_least_once": len(matched_bib_ids),
    "bibliography_entries_requiring_manual_unused_review": len(unused),
    "warning": "First-author/year matching is a review aid, not proof of citation validity or bibliographic accuracy.",
}
(OUT / "citation_crosswalk_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False, indent=2))
