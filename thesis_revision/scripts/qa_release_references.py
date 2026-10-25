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

GUIDE_REFS = ['pages 12–16',
 'page 14',
 'pages 14–16, 76–78, 111–116',
 'pages 19–26',
 'pages 29–31, 84–86',
 'pages 22–25',
 'pages 27–32',
 'pages 25–26',
 'pages 21–22',
 'pages 21–22',
 'pages 50–53',
 'page 54',
 'pages 54–55 et 114',
 'pages 53 et 115',
 'pages 60–61 et 115',
 'pages 59–61',
 'pages 42–44, 59–61 et 94–95',
 'pages 45–47',
 'pages 67–69',
 'page 68',
 'pages 68–69',
 'pages 67–71 et 114–115',
 'pages 70–71',
 'page 70',
 'pages 72–74',
 'pages 42–44, 74–75 et 94–95',
 'pages 67 et 83',
 'pages 44–48 et 75',
 'pages 81 et 115',
 'pages 81 et 86',
 'pages 85–86',
 'pages 82 et 114',
 'pages 88–90',
 'pages 76–77 et 111–112',
 'pages 94–95',
 'pages 95–96',
 'pages 92–93',
 'pages 104–110',
 'pages 16 et 101–103',
 'pages 101–103']
SLIDE_REFS = ['1',
 '12–16',
 '14–16',
 '19–26',
 '27–32',
 '50–53',
 '44, 54–59',
 '42–44, 74–75',
 '45–47, 67–69',
 '68–69',
 '70–77',
 '79–90',
 '91–100',
 '101–103',
 '104–110']
JOURNAL_REFS = ['1',
 '2–4',
 '5–8',
 '9–11',
 '12–16',
 '19–26',
 '21–22',
 '25–26, 104–110',
 '22–37',
 '29–31, 85–87',
 '28–30',
 '38–44',
 '42–44, 59–61, 74–75, 94–96',
 '94–96, 104–110',
 '45–47, 67–69',
 '44–48, 75',
 '45–47, 67–69',
 '50–53, 62–64',
 '53, 115',
 '54–59',
 '56–57, 114',
 '44, 57–58, 114',
 '58, 83, 114',
 '60–61, 115',
 '59–61',
 '65–78',
 '67, 83, 88',
 '67–69, 114',
 '70–71',
 '74–75, 94–96',
 '72–74',
 '75–76, 83–84',
 '79–90',
 '81, 115',
 '82–86',
 '91–100',
 '91–93',
 '92–93',
 '98–100, 111–113',
 '95–96',
 '91–100',
 '101–103',
 '104–110',
 '111–116',
 '1–116']
MAJOR_PAGES = {'INTRODUCTION GÉNÉRALE': 12,
 'CHAPITRE I': 17,
 'CHAPITRE II': 38,
 'CHAPITRE III': 50,
 'CHAPITRE IV': 65,
 'CHAPITRE V': 79,
 'CHAPITRE VI': 91,
 'CONCLUSION GÉNÉRALE': 101,
 'BIBLIOGRAPHIE': 104,
 'ANNEXE A': 111,
 'ANNEXE B': 114}
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
        "visual_review_bibliography_range_is_final": "Bibliographie, pages 104–110" in visual,
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
