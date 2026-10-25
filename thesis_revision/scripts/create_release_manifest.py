#!/usr/bin/env python3
"""Create release hashes and a machine-readable closure audit.

Run after the PDF/DOCX builders and their three content/QA auditors. This script
never changes thesis content; it fails if the recorded evidence is stale or if
a required release/tracking file is missing.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDITS = ROOT / "audits"
DELIVERABLES = ROOT / "deliverables"
RELEASE_DATE = "2026-10-25"

DELIVERABLE_NAMES = [
    "These_revisee_BERKANE_Dhiyaddine.pdf",
    "These_revisee_BERKANE_Dhiyaddine.docx",
    "Journal_des_revisions_BERKANE_Dhiyaddine.md",
    "Guide_de_soutenance_BERKANE_Dhiyaddine.md",
    "LISEZ_MOI.md",
]
AUDIT_NAMES = [
    "build_report.json",
    "docx_build_report.json",
    "final_pdf_qa.json",
    "docx_content_audit.json",
    "revised_citation_audit.json",
    "visual_review.md",
    "registre_etendu_traceability.md",
]
REQUIRED_FILES = [
    "00_cahier_des_charges.md",
    "MEMORY.md",
    "PROGRESS.md",
    "CHANGELOG.md",
    "audits/scientific_review.md",
    "audits/visual_review.md",
    "audits/registre_etendu_traceability.md",
    "audits/pdf_page_inventory.json",
    "source/registre_superviseurs_etendu_ar.md",
    "references/verification_notes.md",
    "references/manual_citation_resolutions.csv",
    "references/bibliography_manual_triage.csv",
    "revision/00_front.md",
    "revision/00_abbreviations.md",
    "revision/09_bibliographie.md",
    "revision/10_annexes.md",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def load(name: str):
    return json.loads((AUDITS / name).read_text(encoding="utf-8"))


def file_record(path: Path) -> dict:
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def requirement_status() -> dict:
    cahier = (ROOT / "00_cahier_des_charges.md").read_text(encoding="utf-8")
    progress = (ROOT / "PROGRESS.md").read_text(encoding="utf-8")
    cahier_ids = set(re.findall(r"^\| (R\d{2}) \|", cahier, flags=re.MULTILINE))
    rows = re.findall(r"^\| (R\d{2}) \| [^|]+ \| ([✅⛔]) \|", progress, flags=re.MULTILINE)
    statuses = {key: value.strip() for key, value in rows}
    expected = {f"R{i:02d}" for i in range(1, 35)}
    completed = sorted(key for key, value in statuses.items() if value == "✅")
    blocked = sorted(key for key, value in statuses.items() if value == "⛔")
    return {
        "expected_ids_present": cahier_ids == expected and set(statuses) == expected,
        "statuses": statuses,
        "completed": completed,
        "blocked": blocked,
    }


def main() -> None:
    pdf_qa = load("final_pdf_qa.json")
    docx_qa = load("docx_content_audit.json")
    citations = load("revised_citation_audit.json")
    build = load("build_report.json")
    docx_build = load("docx_build_report.json")

    deliverables = [file_record(DELIVERABLES / name) for name in DELIVERABLE_NAMES]
    by_name = {Path(item["path"]).name: item for item in deliverables}
    pdf_name = "These_revisee_BERKANE_Dhiyaddine.pdf"
    docx_name = "These_revisee_BERKANE_Dhiyaddine.docx"
    pdf_hash = by_name[pdf_name]["sha256"]
    docx_hash = by_name[docx_name]["sha256"]

    reqs = requirement_status()
    journal = (DELIVERABLES / "Journal_des_revisions_BERKANE_Dhiyaddine.md").read_text(encoding="utf-8")
    guide = (DELIVERABLES / "Guide_de_soutenance_BERKANE_Dhiyaddine.md").read_text(encoding="utf-8")
    readme = (DELIVERABLES / "LISEZ_MOI.md").read_text(encoding="utf-8")
    visual = (AUDITS / "visual_review.md").read_text(encoding="utf-8")
    expanded_register = (ROOT / "source/registre_superviseurs_etendu_ar.md").read_text(encoding="utf-8")
    expanded_trace = (AUDITS / "registre_etendu_traceability.md").read_text(encoding="utf-8")

    def trace_ids(prefix: str, count: int) -> bool:
        expected = [f"{prefix}{i:02d}" for i in range(1, count + 1)]
        return re.findall(rf"^\| ({prefix}\d{{2}}) \|", expanded_trace, flags=re.MULTILINE) == expected

    expanded_register_complete = (
        trace_ids("A", 22)
        and trace_ids("V", 9)
        and trace_ids("U", 17)
        and "## أولًا" in expanded_register
        and "## ثانيًا" in expanded_register
        and "## ثالثًا" in expanded_register
        and "## رابعًا" in expanded_register
        and "## خامسًا" in expanded_register
        and "## سادسًا" in expanded_register
        and "## ملحق خاص بالصور" in expanded_register
        and "R27 وحده محجوب" in expanded_trace
    )

    page_refs: list[int] = []
    for line in guide.splitlines():
        if re.search(r"— pages?\s+\d", line):
            page_refs.extend(int(value) for value in re.findall(r"\d+", line.split("—", 1)[1]))
    for line in journal.splitlines():
        cells = [cell.strip() for cell in line.split("|")]
        if len(cells) >= 5 and re.fullmatch(r"[\d,;\s–-]+", cells[2] or "x") and re.search(r"\d", cells[2]):
            page_refs.extend(int(value) for value in re.findall(r"\d+", cells[2]))
    required_paths = REQUIRED_FILES + [f"deliverables/{name}" for name in DELIVERABLE_NAMES]

    checks = {
        "required_files_present": all((ROOT / name).is_file() for name in required_paths),
        "expanded_register_traceability_complete": expanded_register_complete,
        "all_34_requirement_ids_present": reqs["expected_ids_present"],
        "33_completed_and_only_R27_blocked": len(reqs["completed"]) == 33 and reqs["blocked"] == ["R27"],
        "pdf_qa_pass_and_all_checks_true": pdf_qa["status"] == "pass" and all(pdf_qa["checks"].values()),
        "docx_qa_pass_and_all_checks_true": docx_qa["status"] == "pass" and all(docx_qa["checks"].values()),
        "citation_audit_pass": citations["status"] == "pass",
        "citation_counts_complete": (
            citations["bibliography_entries"] == 65
            and citations["bibliography_entries_cited"] == 65
            and citations["bibliography_entries_uncited"] == 0
            and citations["citation_occurrences_expanded_by_author_year"] == 93
            and citations["resolved_citation_occurrences"] == 93
            and citations["unresolved_citation_occurrences"] == 0
            and not citations["abstract_citation_violations"]
        ),
        "pdf_hash_matches_qa": pdf_hash == pdf_qa["sha256"],
        "docx_hash_matches_qa": docx_hash == docx_qa["sha256"],
        "pdf_hash_propagated_to_human_records": all(pdf_hash in text for text in (journal, readme, visual)),
        "docx_hash_propagated_to_readme": docx_hash in readme,
        "builder_and_qa_page_counts_match": build["pages"] == pdf_qa["pages"] == 98,
        "builder_has_stable_captions_and_no_warnings": (
            build["caption_pages_stable_between_passes"]
            and build["page_count_stable_between_passes"]
            and not build["missing_captions"]
            and not build["unexpected_captions"]
            and not build["warnings"]
        ),
        "docx_builder_counts_match_qa": (
            docx_build["paragraphs"] == docx_qa["paragraphs"]
            and docx_build["tables"] == docx_qa["tables"]
            and docx_build["inline_shapes"] == docx_qa["inline_shapes"]
        ),
        "journal_and_guide_page_references_in_range": bool(page_refs) and all(1 <= n <= 98 for n in page_refs),
        "no_stale_99_page_release_claim": "99 pages" not in (journal + guide + readme + visual),
        "docx_renderer_limit_explicit": "renderer-dependent" in docx_qa["rendering_note"],
        "r27_missing_deck_limit_explicit": "diaporama" in journal and "R27" in journal and "غير مرفق" in readme,
    }

    manifest = {
        "release_id": "BERKANE-Dhiyaddine-revision-2026-10-25",
        "release_date": RELEASE_DATE,
        "artifact_status": "pass" if all(checks.values()) else "fail",
        "requirement_status": "33_completed_1_blocked",
        "reference_document": f"deliverables/{pdf_name}",
        "reference_pagination": {"pages": 98, "paper": "A4", "note": "PDF is authoritative; DOCX pagination is renderer-dependent."},
        "deliverables": deliverables,
        "audit_evidence": [file_record(AUDITS / name) for name in AUDIT_NAMES],
        "scientific_summary": {
            "bibliography_entries": 65,
            "resolved_author_year_occurrences": 93,
            "figures": build["figures"],
            "tables_in_pdf": build["tables"],
            "pdf_outline_entries": build["outline_entries"],
        },
        "source_provenance": {
            "original_thesis": "source/Étude_bibliographique_sur_les_fondations_de_ponts.pdf",
            "original_thesis_sha256": "a2d1ab3b3d8ebfc4a4f9bd954cd3435a8722f09f042cc52ad5a342c7147f5900",
            "expanded_supervisor_register": "source/registre_superviseurs_etendu_ar.md",
            "expanded_supervisor_register_sha256": sha256(ROOT / "source/registre_superviseurs_etendu_ar.md"),
            "expanded_register_coverage": {"thematic_axes": 22, "visual_points": 9, "uncertainty_items": 17},
            "original_archive_sha256": "d169370dbf3d40257d3d60d330838b5e08179956d83689fdfa47ee9a1e55553b",
            "verified_reference_library": "/home/user/thesis-reference-library (outside Git)",
            "library_pdf_count": 2150,
        },
        "known_reservations": [
            "R27 remains blocked: no original slide deck was supplied; the guide contains a proposed plan, not a corrected deck.",
            "No official Larbi Tébessi formatting guide was located; institutional compliance is not claimed.",
            "DOCX package/content are audited, but Word-specific visual pagination was not rendered in this environment.",
            "The work is bibliographic/theoretical and is not presented as fieldwork.",
        ],
        "page_reference_count_checked": len(page_refs),
    }
    (AUDITS / "release_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    closure = {
        "audit_date": RELEASE_DATE,
        "audit_status": "pass" if all(checks.values()) else "fail",
        "release_status": "ready_except_R27" if all(checks.values()) else "not_ready",
        "checks": checks,
        "requirements": {
            "total": 34,
            "completed_count": len(reqs["completed"]),
            "completed_ids": reqs["completed"],
            "blocked_ids": reqs["blocked"],
        },
        "failed_checks": [key for key, value in checks.items() if not value],
        "release_manifest": "audits/release_manifest.json",
        "decision": (
            "Artifact and traceability checks pass. PDF/DOCX and guides may be delivered with the documented reservations. "
            "R27 is not closed until the original slide deck is supplied and corrected."
            if all(checks.values())
            else "Do not present this release as closed until failed checks are resolved and evidence is regenerated."
        ),
    }
    (AUDITS / "closure_audit.json").write_text(json.dumps(closure, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(closure, ensure_ascii=False, indent=2))
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
