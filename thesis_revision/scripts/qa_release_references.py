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
 'pages 14–18',
 'page 16',
 'pages 16–18, 89–93, 133–138',
 'pages 21–27',
 'pages 31–33, 101–103',
 'pages 24–27',
 'pages 29–34',
 'pages 27–28',
 'pages 23–24',
 'pages 23–24',
 'pages 55–59',
 'page 60',
 'pages 60–61 et 136',
 'pages 58 et 137',
 'pages 70–71 et 137',
 'pages 68–71',
 'pages 45–47, 68–71 et 115–116',
 'pages 49–52',
 'pages 79–81',
 'page 80',
 'pages 80–81',
 'pages 79–83 et 136–137',
 'pages 82–83',
 'page 82',
 'pages 84–86',
 'pages 45–47, 87–88 et 115–116',
 'pages 79 et 99',
 'pages 47–53 et 87–88',
 'pages 97 et 137',
 'pages 97 et 103',
 'pages 102–103',
 'pages 98 et 136',
 'pages 106–111',
 'pages 89–90 et 133–134',
 'pages 115–116',
 'pages 116–117',
 'pages 113–114',
 'pages 126–132',
 'pages 18 et 123–125',
 'pages 123–125',
]
SLIDE_REFS = [
 '1',
 '14–18',
 '16–18',
 '21–27',
 '29–34',
 '55–59',
 '47, 60–64',
 '45–47, 87–88',
 '49–52, 79–81',
 '80–81',
 '82–90',
 '95–111',
 '112–122',
 '123–125',
 '126–132',
]
JOURNAL_REFS = [
 '1',
 '2–4',
 '5–10',
 '11–13',
 '14–18',
 '21–27',
 '23–24',
 '27–28, 126–132',
 '24–39',
 '31–33, 102–104',
 '30–32',
 '40–47',
 '45–47, 68–71, 87–88, 115–117',
 '115–117, 126–132',
 '49–52, 79–81',
 '47–53, 87–88',
 '49–52, 79–81',
 '55–59, 71–76',
 '58, 137',
 '60–64',
 '62–63, 136',
 '48, 63–66, 136',
 '66, 99, 136',
 '70–71, 137',
 '68–71',
 '77–94',
 '79, 99, 106–107',
 '79–81, 136',
 '82–83',
 '87–88, 115–117',
 '84–86',
 '87–89, 99–101',
 '95–111',
 '97, 137',
 '98–103',
 '112–122',
 '112–114',
 '113–114',
 '119–122, 133–135',
 '116–117',
 '112–122',
 '123–125',
 '126–132',
 '133–138',
 '1–138',
]
MAJOR_PAGES = {'ANNEXE A': 133,
 'ANNEXE B': 136,
 'BIBLIOGRAPHIE': 126,
 'CHAPITRE I': 19,
 'CHAPITRE II': 40,
 'CHAPITRE III': 55,
 'CHAPITRE IV': 77,
 'CHAPITRE V': 95,
 'CHAPITRE VI': 112,
 'CONCLUSION GÉNÉRALE': 123,
 'INTRODUCTION GÉNÉRALE': 14}
ARABIC_CAPTION_REFS = {
    "A07": [("Figure", "I.3")],
    "A08": [("Figure", "I.4")],
    "A11": [("Figure", "IV.6")],
    "A12": [("Tableau", "III.3")],
    "A14": [("Figure", "III.10")],
    "A17": [("Figure", "V.3")],
    "A18": [("Figure", "IV.2")],
    "A21": [("Figure", "VI.1")],
    "V01": [("Figure", "I.4")],
    "V05": [("Figure", "I.1"), ("Figure", "I.2")],
    "V06": [("Figure", "IV.2")],
    "V07": [("Figure", "II.6")],
    "V08": [("Figure", "III.10")],
    "V09": [("Figure", "I.3")],
}
V03_FIGURES = ["I.1", "II.6", "IV.1", "IV.2", "IV.3", "IV.4"]


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
        "visual_review_bibliography_range_is_final": "Bibliographie, pages 126–132" in visual,
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
