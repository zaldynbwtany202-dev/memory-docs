#!/usr/bin/env python3
"""Audit human-facing page references against the final PDF/build evidence.

The expected topic references are curated after reading the final PDF. Caption
references and major-part starts are also derived independently from the build
report and the PDF outline, so a stale or cascaded page replacement fails loudly.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
AUDITS = ROOT / "audits"
DELIVERABLES = ROOT / "deliverables"
PDF = DELIVERABLES / "These_revisee_BERKANE_Dhiyaddine.pdf"

GUIDE_REFS = [
    "pages 12–16", "page 14", "pages 14–16, 70–72, 104–109",
    "pages 19–26", "pages 29–31, 78–80", "pages 22–25",
    "pages 27–32", "pages 25–26", "pages 21–22", "pages 21–22",
    "pages 45–48", "page 49", "pages 49–50 et 107", "pages 48 et 108",
    "pages 55–56 et 108", "pages 54–56", "pages 38–40, 54–56 et 87–88",
    "pages 41–42", "pages 61–63", "page 62", "pages 62–63",
    "pages 61–65 et 107–108", "pages 64–65", "page 64",
    "pages 66–68", "pages 38–40, 68–69 et 87–88", "pages 61 et 77",
    "pages 40–43 et 69", "pages 75 et 108", "pages 75 et 80",
    "pages 79–80", "pages 76 et 107", "pages 82–83",
    "pages 70–71 et 104–105", "pages 87–88", "pages 88–89",
    "pages 85–86", "pages 97–103", "pages 16 et 94–96", "pages 94–96",
]
SLIDE_REFS = [
    "1", "12–16", "14–16", "19–26", "27–32", "45–48", "40, 49–54",
    "38–40, 68–69", "41–42, 61–63", "62–63", "64–71", "73–83",
    "84–93", "94–96", "97–103",
]
JOURNAL_REFS = [
    "1", "2–4", "5–8", "9–11", "12–16", "19–26", "21–22",
    "25–26, 97–103", "22–33", "29–31, 79–81", "28–30", "34–40",
    "38–40, 54–56, 68–69, 87–89", "87–89, 97–103", "41–42, 61–63",
    "40–43, 69", "41–42, 61–63", "45–48, 57–58", "48, 108", "49–54",
    "51–52, 107", "40, 52–53, 107", "53, 77, 107", "55–56, 108",
    "54–56", "59–72", "61, 77, 82", "61–63, 107", "64–65",
    "68–69, 87–89", "66–68", "69–70, 77–78", "73–83", "75, 108",
    "76–80", "84–93", "84–86", "85–86", "91–93, 104–106", "88–89",
    "84–93", "94–96", "97–103", "104–109", "1–109",
]
MAJOR_PAGES = {
    "INTRODUCTION GÉNÉRALE": 12,
    "CHAPITRE I": 17,
    "CHAPITRE II": 34,
    "CHAPITRE III": 45,
    "CHAPITRE IV": 59,
    "CHAPITRE V": 73,
    "CHAPITRE VI": 84,
    "CONCLUSION GÉNÉRALE": 94,
    "BIBLIOGRAPHIE": 97,
    "ANNEXE A": 104,
    "ANNEXE B": 107,
}
ARABIC_CAPTION_REFS = {
    "A07": [("Figure", "I.3")],
    "A08": [("Figure", "I.4")],
    "A11": [("Figure", "IV.5")],
    "A12": [("Tableau", "III.3")],
    "A14": [("Figure", "III.3")],
    "A17": [("Figure", "V.2")],
    "A18": [("Figure", "IV.2")],
    "A21": [("Figure", "VI.1")],
    "V01": [("Figure", "I.4")],
    "V05": [("Figure", "I.1"), ("Figure", "I.2")],
    "V06": [("Figure", "IV.2")],
    "V07": [("Figure", "II.3")],
    "V08": [("Figure", "III.3")],
    "V09": [("Figure", "I.3")],
}
V03_FIGURES = ["I.1", "II.3", "IV.1", "IV.2", "IV.3", "IV.4"]


def main() -> None:
    build = json.loads((AUDITS / "build_report.json").read_text(encoding="utf-8"))
    captions = build["caption_pages"]
    guide = (DELIVERABLES / "Guide_de_soutenance_BERKANE_Dhiyaddine.md").read_text(encoding="utf-8")
    journal = (DELIVERABLES / "Journal_des_revisions_BERKANE_Dhiyaddine.md").read_text(encoding="utf-8")
    trace = (AUDITS / "registre_etendu_traceability.md").read_text(encoding="utf-8")
    visual = (AUDITS / "visual_review.md").read_text(encoding="utf-8")

    questions = []
    for line in guide.splitlines():
        match = re.match(r"^\*\*(\d+)\.\s+(.+?) — (pages? .+?)\*\*\s*$", line)
        if match:
            questions.append((int(match.group(1)), match.group(3)))
    question_refs = [ref for _, ref in questions]

    slides = []
    for line in guide.splitlines():
        match = re.match(r"^\| (\d+) \|.*\| ([^|]+?) \|$", line)
        if match:
            slides.append((int(match.group(1)), match.group(2).strip()))
    slide_refs = [ref for _, ref in slides]

    revision_refs = []
    for line in journal.splitlines():
        cells = [cell.strip() for cell in line.split("|")]
        if len(cells) >= 6 and re.fullmatch(r"R\d\d(?:, R\d\d)*", cells[3]):
            revision_refs.append(cells[2])

    trace_rows = {
        match.group(1): match.group(0)
        for match in re.finditer(r"^\| ([AV]\d{2}) \|.*$", trace, flags=re.MULTILINE)
    }
    caption_failures = []
    verified_caption_refs = []
    for row_id, expected in ARABIC_CAPTION_REFS.items():
        row = trace_rows.get(row_id, "")
        for kind, number in expected:
            key = f"{kind} {number}"
            page = captions.get(key)
            arabic_label = "الشكل" if kind == "Figure" else "الجدول"
            token = f"{arabic_label} {number} ص{page}"
            if page is None or token not in row:
                caption_failures.append({"row": row_id, "caption": key, "expected_token": token})
            else:
                verified_caption_refs.append({"row": row_id, "caption": key, "page": page})

    v03 = trace_rows.get("V03", "")
    v03_actual = [
        (f"{roman}.{number}", int(page))
        for roman, number, page in re.findall(r"(?<![A-Z])(I{1,3}|IV|V|VI)\.(\d+) ص(\d+)", v03)
    ]
    v03_expected = [(number, captions[f"Figure {number}"]) for number in V03_FIGURES]

    with pymupdf.open(PDF) as document:
        toc = document.get_toc(simple=True)
    actual_major = {}
    for prefix in MAJOR_PAGES:
        matches = [
            page for _, title, page in toc
            if re.match(rf"^{re.escape(prefix)}(?=$|\s*[—-])", title.strip().upper())
        ]
        actual_major[prefix] = matches

    visual_match = re.search(r"leurs pages finales sont ([^.]+)\.", visual)
    visual_figure_pages = [int(value) for value in re.findall(r"\d+", visual_match.group(1))] if visual_match else []
    build_figure_pages = sorted(page for key, page in captions.items() if key.startswith("Figure "))

    checks = {
        "guide_40_question_references_match_curated_final_pdf": (
            [number for number, _ in questions] == list(range(1, 41))
            and question_refs == GUIDE_REFS
            and "scénario de débit ou un débit de pointe" in guide
            and "débit de projet" not in guide
        ),
        "guide_15_slide_references_match_curated_final_pdf": (
            [number for number, _ in slides] == list(range(1, 16))
            and slide_refs == SLIDE_REFS
        ),
        "journal_45_revision_references_match_curated_final_pdf": revision_refs == JOURNAL_REFS,
        "arabic_caption_references_match_build_report": not caption_failures and len(verified_caption_refs) == 15,
        "arabic_v03_has_no_replacement_cascade": v03_actual == v03_expected,
        "major_part_starts_match_pdf_outline": all(
            actual_major[prefix] == [page] for prefix, page in MAJOR_PAGES.items()
        ),
        "visual_review_lists_all_final_figure_pages": visual_figure_pages == build_figure_pages,
        "visual_review_bibliography_range_is_final": "Bibliographie, pages 97–103" in visual,
    }
    report = {
        "status": "pass" if all(checks.values()) else "fail",
        "pdf": PDF.relative_to(ROOT).as_posix(),
        "pages": build["pages"],
        "checks": checks,
        "counts": {
            "guide_questions": len(questions),
            "slide_rows": len(slides),
            "journal_revision_rows": len(revision_refs),
            "arabic_caption_references": len(verified_caption_refs),
            "visual_figure_pages": len(visual_figure_pages),
        },
        "major_pages_expected": MAJOR_PAGES,
        "major_pages_actual": actual_major,
        "v03_expected": v03_expected,
        "v03_actual": v03_actual,
        "caption_failures": caption_failures,
        "verified_caption_references": verified_caption_refs,
        "note": "Topic ranges are curated from the final PDF; caption pages and major-part starts are independently derived from build/PDF evidence.",
    }
    destination = AUDITS / "release_reference_audit.json"
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
