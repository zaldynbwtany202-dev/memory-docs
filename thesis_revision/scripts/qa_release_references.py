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

GUIDE_REFS = ['pages 13–17',
 'page 15',
 'pages 15–17, 80–84, 119–124',
 'pages 20–27',
 'pages 30–32, 90–92',
 'pages 23–26',
 'pages 28–33',
 'pages 26–27',
 'pages 22–23',
 'pages 22–23',
 'pages 52–55',
 'page 56',
 'pages 56–57 et 122',
 'pages 55 et 123',
 'pages 62–63 et 123',
 'pages 61–63',
 'pages 43–45, 61–63 et 101–102',
 'pages 46–49',
 'pages 71–73',
 'page 72',
 'pages 72–73',
 'pages 71–75 et 122–123',
 'pages 74–75',
 'page 74',
 'pages 76–78',
 'pages 43–45, 78–79 et 101–102',
 'pages 71 et 89',
 'pages 45–50 et 79',
 'pages 87 et 123',
 'pages 87 et 92',
 'pages 91–92',
 'pages 88 et 122',
 'pages 94–97',
 'pages 80–81 et 119–120',
 'pages 101–102',
 'pages 102–103',
 'pages 99–100',
 'pages 112–118',
 'pages 17 et 109–111',
 'pages 109–111']
SLIDE_REFS = ['1',
 '13–17',
 '15–17',
 '20–27',
 '28–33',
 '52–55',
 '45, 56–61',
 '43–45, 78–79',
 '46–49, 71–73',
 '72–73',
 '74–81',
 '85–97',
 '98–108',
 '109–111',
 '112–118']
JOURNAL_REFS = ['1',
 '2–4',
 '5–9',
 '10–12',
 '13–17',
 '20–27',
 '22–23',
 '26–27, 112–118',
 '23–38',
 '30–32, 91–93',
 '29–31',
 '39–45',
 '43–45, 61–63, 78–79, 101–103',
 '101–103, 112–118',
 '46–49, 71–73',
 '45–50, 79',
 '46–49, 71–73',
 '52–55, 64–68',
 '55, 123',
 '56–61',
 '58–59, 122',
 '45, 59–60, 122',
 '60, 89, 122',
 '62–63, 123',
 '61–63',
 '69–84',
 '71, 89, 94',
 '71–73, 122',
 '74–75',
 '78–79, 101–103',
 '76–78',
 '79–80, 89–90',
 '85–97',
 '87, 123',
 '88–92',
 '98–108',
 '98–100',
 '99–100',
 '105–108, 119–121',
 '102–103',
 '98–108',
 '109–111',
 '112–118',
 '119–124',
 '1–124']
MAJOR_PAGES = {'ANNEXE A': 119,
 'ANNEXE B': 122,
 'BIBLIOGRAPHIE': 112,
 'CHAPITRE I': 18,
 'CHAPITRE II': 39,
 'CHAPITRE III': 52,
 'CHAPITRE IV': 69,
 'CHAPITRE V': 85,
 'CHAPITRE VI': 98,
 'CONCLUSION GÉNÉRALE': 109,
 'INTRODUCTION GÉNÉRALE': 13}
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
        "visual_review_bibliography_range_is_final": "Bibliographie, pages 112–118" in visual,
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
