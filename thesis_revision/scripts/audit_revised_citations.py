#!/usr/bin/env python3
"""Bidirectional citation audit for the revised thesis Markdown sources.

The audit is deliberately explicit: it recognizes the controlled author--year
style used in the revision, records file/line evidence, and fails if a citation
is unresolved or a bibliography entry is never cited. Event dates and standard
numbers are not treated as citations unless an author/organization is present.
"""
from __future__ import annotations

import csv
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "revision"
OUT = ROOT / "audits"
MAIN_FILES = [
    "01_introduction.md", "02_chapitre_I.md", "03_chapitre_II.md",
    "04_chapitre_III.md", "05_chapitre_IV.md", "06_chapitre_V.md",
    "07_chapitre_VI.md", "08_conclusion.md", "10_annexes.md",
]
YEAR = r"(?:19|20)\d{2}[a-z]?|s\.\s*d\."
YEARS = rf"(?:{YEAR})(?:\s*,\s*(?:{YEAR}))*"
TOKEN = r"[A-ZÀ-ÞĆČĎĚĹĽŇŔŠŤŮÝŽ][A-ZÀ-ÞĆČĎĚĹĽŇŔŠŤŮÝŽ0-9’'\-]*"
NAME = rf"{TOKEN}(?:\s+{TOKEN}){{0,5}}"
AUTHORS = rf"{NAME}(?:\s+et\s+(?:al\.|{TOKEN}(?:\s+{TOKEN}){{0,3}}))?"
NARRATIVE = re.compile(rf"(?<![\w’'\-])(?P<authors>{AUTHORS})\s*\((?P<years>{YEARS})\)")
PARENTHETICAL = re.compile(r"\((?P<content>[^()\n]{1,400})\)")
PARENT_SEGMENT = re.compile(rf"^(?P<authors>.+?),\s*(?P<years>{YEARS})$")
YEAR_FIND = re.compile(YEAR)


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = "".join(char for char in value if not unicodedata.combining(char))
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def first_author(authors: str) -> str:
    authors = re.sub(r"\s*\(dir\.\)\s*", " ", authors).strip()
    return authors.split(",", 1)[0].strip()


def explicit_first_author(cited_authors: str) -> str:
    value = re.split(r"\s+et\s+(?:al\.|)" + TOKEN, cited_authors, maxsplit=1)[0]
    # The expression above handles both "et al." and "et SECOND-AUTEUR".
    if value == cited_authors:
        value = re.split(r"\s+et\s+", cited_authors, maxsplit=1)[0]
    return value.strip(" ,;")


def aliases_for(author: str) -> set[str]:
    aliases = {author}
    if author == "ASTM INTERNATIONAL":
        aliases.add("ASTM")
    if author == "MÉNARD":
        aliases.add("MENARD")
    return aliases


def controlled_narrative(authors: str) -> bool:
    """Reject ordinary mixed-case words accidentally preceding a bare year."""
    words = authors.replace("et al.", "").replace(" et ", " ").split()
    return bool(words) and all(word.upper() == word for word in words)


bib_text = (CONTENT / "09_bibliographie.md").read_text(encoding="utf-8")
raw_entries = re.findall(r"\[\[REF:(.*?)\]\]", bib_text, flags=re.S)
entries: list[dict[str, object]] = []
alias_index: dict[tuple[str, str], list[int]] = defaultdict(list)
for number, raw in enumerate(raw_entries, 1):
    match = re.match(rf"\s*(?P<authors>.+?)\s*\((?P<year>{YEAR})\)\.", raw, flags=re.S)
    if not match:
        raise ValueError(f"Unparseable bibliography entry B{number:03d}: {raw[:100]}")
    authors = match.group("authors").strip()
    first = first_author(authors)
    year = re.sub(r"\s+", " ", match.group("year"))
    entry = {
        "id": f"B{number:03d}", "authors": authors, "first_author": first,
        "year": year, "text": re.sub(r"\s+", " ", raw).strip(),
    }
    entries.append(entry)
    for alias in aliases_for(first):
        key = (normalize(alias), normalize(year))
        if number - 1 not in alias_index[key]:
            alias_index[key].append(number - 1)

ambiguous = {key: ids for key, ids in alias_index.items() if len(ids) > 1}
if ambiguous:
    raise ValueError(f"Ambiguous bibliography aliases: {ambiguous}")

citations: list[dict[str, object]] = []
unresolved: list[dict[str, object]] = []
cited_entry_ids: set[int] = set()


def record(filename: str, line_number: int, line: str, authors: str, years: str, raw: str, form: str) -> None:
    first = explicit_first_author(authors)
    for year in YEAR_FIND.findall(years):
        normalized_year = re.sub(r"\s+", " ", year)
        key = (normalize(first), normalize(normalized_year))
        base = {
            "file": filename, "line": line_number, "form": form,
            "authors_raw": authors, "first_author": first, "year": normalized_year,
            "raw": raw, "context": re.sub(r"\s+", " ", line).strip(),
        }
        ids = alias_index.get(key, [])
        if not ids:
            unresolved.append({**base, "reason": "no bibliography alias/year match"})
            citations.append({**base, "bibliography_id": "", "status": "unresolved"})
        else:
            entry_index = ids[0]
            cited_entry_ids.add(entry_index)
            citations.append({**base, "bibliography_id": entries[entry_index]["id"], "status": "resolved"})


for filename in MAIN_FILES:
    for line_number, line in enumerate((CONTENT / filename).read_text(encoding="utf-8").splitlines(), 1):
        occupied: list[tuple[int, int]] = []
        for match in NARRATIVE.finditer(line):
            authors = match.group("authors").strip()
            if not controlled_narrative(authors):
                continue
            record(filename, line_number, line, authors, match.group("years"), match.group(0), "narrative")
            occupied.append(match.span())
        for match in PARENTHETICAL.finditer(line):
            # Do not reinterpret the year list of an already recognized
            # narrative citation as a new parenthetical author–year citation.
            if any(match.start() < end and match.end() > start for start, end in occupied):
                continue
            # Parenthetical citations have an author/organization and a comma;
            # narrative bare-year groups were already processed above.
            content = match.group("content").strip()
            if "," not in content:
                continue
            for segment in re.split(r"\s*;\s*", content):
                segment_match = PARENT_SEGMENT.fullmatch(segment.strip())
                if not segment_match:
                    continue
                authors = segment_match.group("authors").strip()
                if not controlled_narrative(re.split(r"\s+et\s+", authors)[0]):
                    continue
                record(filename, line_number, line, authors, segment_match.group("years"), match.group(0), "parenthetical")

fields = ["bibliography_id", "status", "file", "line", "form", "authors_raw", "first_author", "year", "raw", "context"]
with (OUT / "revised_citation_occurrences.csv").open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields)
    writer.writeheader()
    writer.writerows(citations)
with (OUT / "revised_unresolved_citations.csv").open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(unresolved[0].keys()) if unresolved else fields + ["reason"])
    writer.writeheader()
    writer.writerows(unresolved)

usage_rows = []
for index, entry in enumerate(entries):
    occurrences = [row for row in citations if row.get("bibliography_id") == entry["id"]]
    usage_rows.append({
        "bibliography_id": entry["id"], "first_author": entry["first_author"], "year": entry["year"],
        "citation_count": len(occurrences),
        "locations": ";".join(f"{row['file']}:{row['line']}" for row in occurrences),
        "status": "cited" if occurrences else "uncited",
        "entry": entry["text"],
    })
with (OUT / "revised_bibliography_usage.csv").open("w", encoding="utf-8", newline="") as handle:
    fields_usage = ["bibliography_id", "first_author", "year", "citation_count", "locations", "status", "entry"]
    writer = csv.DictWriter(handle, fieldnames=fields_usage)
    writer.writeheader()
    writer.writerows(usage_rows)

# Abstracts must remain citation-free in all three languages.
front = (CONTENT / "00_front.md").read_text(encoding="utf-8")
abstract_violations = []
current = ""
for line_number, line in enumerate(front.splitlines(), 1):
    if line.startswith("# "):
        current = line[2:].strip()
    if current in {"RÉSUMÉ", "ABSTRACT", "الملخص"}:
        if re.search(r"\[\[REF:|\bdoi\b|https?://|\([^()\n]*(?:" + YEAR + r")[^()\n]*\)", line, flags=re.I):
            abstract_violations.append({"section": current, "line": line_number, "text": line})
        if NARRATIVE.search(line):
            abstract_violations.append({"section": current, "line": line_number, "text": line})

uncited = [row for row in usage_rows if row["status"] == "uncited"]
summary = {
    "main_files_audited": MAIN_FILES,
    "bibliography_entries": len(entries),
    "bibliography_entries_cited": len(cited_entry_ids),
    "bibliography_entries_uncited": len(uncited),
    "citation_occurrences_expanded_by_author_year": len(citations),
    "resolved_citation_occurrences": len(citations) - len(unresolved),
    "unresolved_citation_occurrences": len(unresolved),
    "abstract_citation_violations": abstract_violations,
    "uncited_entries": [{"bibliography_id": row["bibliography_id"], "author": row["first_author"], "year": row["year"]} for row in uncited],
    "status": "pass" if not unresolved and not uncited and not abstract_violations else "fail",
    "scope_note": "Controlled author–year audit of revised Markdown sources; event dates and standard designations without an author are intentionally excluded.",
}
(OUT / "revised_citation_audit.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False, indent=2))
raise SystemExit(0 if summary["status"] == "pass" else 2)
