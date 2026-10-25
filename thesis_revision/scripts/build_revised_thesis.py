#!/usr/bin/env python3
"""Build the revised thesis PDF from traceable Markdown sources.

The builder uses two passes so the lists of figures and tables contain the real
PDF page numbers. FPDF's native TOC placeholder is used for the section outline.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import re
import sys
import tempfile
import warnings
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

import pymupdf
from fontTools.ttLib import TTFont
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from fpdf.fonts import FontFace
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "revision"
ASSETS = ROOT / "assets"
DELIVERABLES = ROOT / "deliverables"
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
SOURCE_PDF = ROOT / "source" / "Étude_bibliographique_sur_les_fondations_de_ponts.pdf"
MARGIN_MM = 25
BODY_SIZE_PT = 12
BODY_LINE_MM = 7.3  # Word-compatible 1.5 spacing for 12 pt Times New Roman.
BODY_FILES = [
    "01_introduction.md", "02_chapitre_I.md", "03_chapitre_II.md",
    "04_chapitre_III.md", "05_chapitre_IV.md", "06_chapitre_V.md",
    "07_chapitre_VI.md", "08_conclusion.md", "09_bibliographie.md",
    "10_annexes.md",
]
ROMAN_RE = re.compile(r"^CHAPITRE\s+([IVXLCDM]+)\b", re.I)
FIG_RE = re.compile(r"^\[\[FIGURE:([a-zA-Z0-9_\-]+)\|(.+)\]\]$")
TABLE_RE = re.compile(r"^\[\[TABLE:([^|\]]+)(?:\|([0-9.,]+))?\]\]$")
EQ_RE = re.compile(r"^\[\[EQ:(.+)\]\]$")
SOURCE_RE = re.compile(r"^\[\[SOURCE:(.+)\]\]$")
REF_RE = re.compile(r"^\[\[REF:(.+)\]\]$")


@dataclass
class CaptionTemplate:
    label: str
    title: str
    kind: str
    asset: str = ""


@dataclass
class ScanResult:
    captions: list[CaptionTemplate] = field(default_factory=list)
    outline_count: int = 0


def read(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Required content file is missing: {path}")
    return path.read_text(encoding="utf-8")


def chapter_from_heading(text: str) -> str | None:
    match = ROMAN_RE.match(text.strip())
    if match:
        return match.group(1).upper()
    if text.startswith("ANNEXE A"):
        return "A"
    if text.startswith("ANNEXE B"):
        return "B"
    return None


def install_times_new_roman(pdf: FPDF):
    """Reuse the source thesis's editable-embedded Times New Roman fonts.

    The source PDF contains subsetted fonts with editable-embedding permission
    (OS/2 fsType=8). They are extracted to a temporary build directory only;
    no standalone proprietary font files are added to the repository. DejaVu
    is registered as a glyph fallback for characters absent from those subsets.
    """
    temporary = tempfile.TemporaryDirectory(prefix="thesis-tnr-")
    font_dir = Path(temporary.name)
    provenance = []
    with pymupdf.open(SOURCE_PDF) as source:
        for xref, style, filename in ((245, "", "regular.ttf"), (267, "B", "bold.ttf"), (280, "I", "italic.ttf")):
            name, extension, _, data = source.extract_font(xref)
            if not data or extension != "ttf" or "Times New Roman" not in name:
                raise ValueError(f"Times New Roman extraction failed at source xref {xref}: {name}")
            font = TTFont(io.BytesIO(data))
            fs_type = font["OS/2"].fsType if "OS/2" in font else None
            if fs_type is None or fs_type & 0x0002:
                raise ValueError(f"Font embedding is not permitted at source xref {xref}: fsType={fs_type}")
            path = font_dir / filename
            path.write_bytes(data)
            pdf.add_font("Serif", style, str(path))
            provenance.append({
                "source_xref": xref, "font": name, "style": style or "regular",
                "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
                "os2_fsType": fs_type, "storage": "temporary build directory only",
            })
    for family, regular, bold in (
        ("FallbackSerif", "DejaVuSerif.ttf", "DejaVuSerif-Bold.ttf"),
        ("Sans", "DejaVuSans.ttf", "DejaVuSans-Bold.ttf"),
    ):
        pdf.add_font(family, "", str(FONT_DIR / regular))
        pdf.add_font(family, "B", str(FONT_DIR / bold))
    pdf.set_fallback_fonts(["FallbackSerif", "Sans"], exact_match=False)
    return temporary, provenance


def scan_content() -> ScanResult:
    result = ScanResult()
    chapter = ""
    counts: dict[tuple[str, str], int] = defaultdict(int)
    for filename in BODY_FILES:
        for raw in read(CONTENT / filename).splitlines():
            line = raw.strip()
            if line.startswith("# "):
                heading = line[2:].strip()
                result.outline_count += 1
                chapter = chapter_from_heading(heading) or ""
            elif line.startswith("## "):
                result.outline_count += 1
            elif line.startswith("### "):
                # Third-level headings remain in the document but not in the compact TOC.
                pass
            fig = FIG_RE.match(line)
            tab = TABLE_RE.match(line)
            if fig:
                if not chapter:
                    raise ValueError(f"Figure outside a numbered chapter in {filename}: {line}")
                key = ("Figure", chapter)
                counts[key] += 1
                label = f"Figure {chapter}.{counts[key]}"
                result.captions.append(CaptionTemplate(label, fig.group(2).strip(), "Figure", fig.group(1)))
            if tab:
                if not chapter:
                    raise ValueError(f"Numbered table outside a chapter in {filename}: {line}")
                key = ("Tableau", chapter)
                counts[key] += 1
                label = f"Tableau {chapter}.{counts[key]}"
                result.captions.append(CaptionTemplate(label, tab.group(1).strip(), "Tableau"))
    return result


class ThesisPDF(FPDF):
    def __init__(self, previous_pages: dict[str, int] | None = None):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_margins(MARGIN_MM, MARGIN_MM, MARGIN_MM)
        self.set_auto_page_break(True, MARGIN_MM)
        self.set_text_shaping(True)
        self._font_tempdir, self.font_provenance = install_times_new_roman(self)
        self.set_font("Serif", "", BODY_SIZE_PT)
        self.set_line_width(0.2)
        self.current_chapter = ""
        self.current_part = ""
        self.header_text = ""
        self.arabic_mode = False
        self.in_cover = True
        self.counts: dict[tuple[str, str], int] = defaultdict(int)
        self.caption_pages: dict[str, int] = {}
        self.previous_pages = previous_pages or {}
        self.links: dict[str, int] = {}
        self.warnings: list[str] = []
        self.continue_current_page = False

    def multi_cell(self, *args, **kwargs):
        # Document paragraphs flow down the page; FPDF's default would otherwise
        # leave the cursor at the right edge and break the next full-width call.
        kwargs.setdefault("new_x", XPos.LMARGIN)
        kwargs.setdefault("new_y", YPos.NEXT)
        return super().multi_cell(*args, **kwargs)

    @property
    def content_width(self) -> float:
        return self.w - self.l_margin - self.r_margin

    def header(self):
        if self.page_no() == 1 or self.in_cover or not self.header_text:
            return
        self.set_y(9)
        header_text = self.header_text
        header_size = 9.0
        self.set_font("Serif", "", header_size)
        available = self.content_width - 4
        while header_size > 8 and self.get_string_width(header_text) > available:
            header_size -= 0.5
            self.set_font("Serif", "", header_size)
        while header_text and self.get_string_width(header_text + " …") > available:
            header_text = header_text[:-1].rstrip()
        if header_text != self.header_text:
            header_text += " …"
        self.set_text_color(90, 100, 105)
        self.cell(0, 5, header_text, align="R")
        self.set_draw_color(180, 190, 195)
        self.line(self.l_margin, 15, self.w - self.r_margin, 15)
        self.set_text_color(0, 0, 0)
        self.set_x(self.l_margin)
        # FPDF does not restore y after header(); without this reset, pages
        # created by automatic breaks start body text inside the running header.
        self.set_y(MARGIN_MM)

    def footer(self):
        if self.page_no() == 1 or self.in_cover:
            return
        self.set_y(-15)
        self.set_font("Serif", "", 10)
        self.set_text_color(80, 80, 80)
        self.cell(0, 6, str(self.page_no()), align="C")
        self.set_text_color(0, 0, 0)

    def add_content_page(self):
        self.in_cover = False
        self.add_page()
        self.set_x(self.l_margin)
        self.set_y(MARGIN_MM)

    def ensure_space(self, needed: float):
        if self.get_y() + needed > self.page_break_trigger:
            self.add_page()
            self.set_x(self.l_margin)
            self.set_y(MARGIN_MM)

    def set_rtl(self, enabled: bool):
        self.arabic_mode = enabled
        if enabled:
            self.set_text_shaping(True, direction="rtl", script="arab", language="ar")
        else:
            self.set_text_shaping(True)

    def add_cover(self):
        self.in_cover = True
        self.header_text = ""
        self.add_page()
        self.set_y(30)
        self.set_font("Serif", "B", 12)
        self.multi_cell(0, 7, "République Algérienne Démocratique et Populaire", align="C")
        self.multi_cell(0, 7, "Ministère de l’Enseignement Supérieur et de la Recherche Scientifique", align="C")
        self.ln(8)
        logo1 = ASSETS / "cover_logo_1.png"
        logo2 = ASSETS / "cover_logo_2.jpeg"
        if logo1.exists():
            self.image(str(logo1), x=35, y=self.get_y(), w=23)
        if logo2.exists():
            self.image(str(logo2), x=151, y=self.get_y(), w=30)
        self.set_y(self.get_y() + 30)
        self.set_font("Serif", "B", 12)
        for text in [
            "Université Larbi Tébessi – Tébessa",
            "Faculté des Sciences Exactes, des Sciences de la Nature et de la Vie",
            "Département des Sciences de la Terre et de l’Univers",
        ]:
            self.multi_cell(0, 6.5, text, align="C")
        self.ln(11)
        self.set_font("Serif", "", 11)
        self.multi_cell(0, 6, "Mémoire présenté en vue de l’obtention du diplôme de", align="C")
        self.ln(3)
        self.set_font("Serif", "B", 21)
        self.multi_cell(0, 10, "MASTER", align="C")
        self.ln(6)
        self.set_font("Serif", "", 11)
        self.multi_cell(0, 6, "Filière : Géologie", align="C")
        self.multi_cell(0, 6, "Option : Géologie de l’Ingénieur et Géotechnique", align="C")
        self.ln(9)
        # Editable title replacing the rasterized title and stray dash line.
        x, y, w, h = self.l_margin + 5, self.get_y(), self.content_width - 10, 29
        self.set_fill_color(245, 248, 250)
        self.set_draw_color(70, 90, 100)
        self.rect(x, y, w, h, style="DF", round_corners=True, corner_radius=3)
        self.set_xy(x + 5, y + 5)
        self.set_font("Serif", "B", 16)
        self.multi_cell(w - 10, 8, "Particularités de la reconnaissance géotechnique des ponts", align="C")
        self.set_x(x + 5)
        self.set_font("Serif", "", 11)
        self.multi_cell(w - 10, 7, "(Étude bibliographique)", align="C")
        self.set_y(y + h + 10)
        self.set_font("Serif", "B", 11)
        self.multi_cell(0, 7, "Présenté par : BERKANE Dhiyaddine", align="C")
        self.ln(6)
        self.multi_cell(0, 7, "Devant le jury :", align="C")
        self.ln(2)
        jury = [
            ("Pr BAALI Fathi", "Professeur", "U.L.T. Tébessa", "Président"),
            ("Pr FEHDI Chems eddine", "Professeur", "U.L.T. Tébessa", "Examinateur"),
            ("Dr MOUICI Ridha", "M.C. « B »", "U.L.T. Tébessa", "Promoteur, Rapporteur"),
            ("Dr AOUN Mounira", "M.C. « B »", "U.L.T. Tébessa", "Co-promoteur"),
        ]
        self.set_font("Serif", "", 8.5)
        widths = [42, 28, 36, 48]
        for row in jury:
            x0 = self.l_margin + 4
            self.set_x(x0)
            for value, width in zip(row, widths):
                self.cell(width, 5.5, value)
            self.ln(5.5)
        self.ln(4)
        self.set_font("Serif", "B", 10)
        self.multi_cell(0, 6, "Session Juin 2026", align="C")
        self.in_cover = False

    def add_major_heading(self, text: str, toc: bool = True):
        # Chapter-opening pages must not inherit the preceding running header.
        self.header_text = ""
        if self.continue_current_page:
            self.continue_current_page = False
            self.set_x(self.l_margin)
            self.set_y(MARGIN_MM)
        else:
            self.add_content_page()
        self.current_part = text
        chapter = chapter_from_heading(text)
        if chapter:
            self.current_chapter = chapter
            self.header_text = text
        elif text.startswith("INTRODUCTION"):
            self.current_chapter = ""
            self.header_text = "INTRODUCTION GÉNÉRALE"
        elif text.startswith("CONCLUSION"):
            self.current_chapter = ""
            self.header_text = "CONCLUSION GÉNÉRALE"
        elif text.startswith("BIBLIOGRAPHIE"):
            self.current_chapter = ""
            self.header_text = "BIBLIOGRAPHIE"
        elif text.startswith("ANNEXE"):
            self.header_text = text
        else:
            self.header_text = ""
        self.set_rtl(text.strip() == "الملخص")
        self.set_font("Sans" if self.arabic_mode else "Serif", "B", 14)
        self.set_text_color(31, 78, 121)
        self.multi_cell(0, 8, text, align="C" if self.arabic_mode else "L")
        self.set_text_color(0, 0, 0)
        self.set_draw_color(31, 78, 121)
        self.line(self.l_margin, self.get_y() + 1, self.w - self.r_margin, self.get_y() + 1)
        self.ln(7)
        front_heading = text.strip() in {"RÉSUMÉ", "ABSTRACT", "الملخص", "LISTE DES ABRÉVIATIONS"}
        if toc and not front_heading:
            self.start_section(text, level=0)

    def add_heading(self, text: str, level: int):
        self.ensure_space(28 if level == 2 else 22)
        self.set_font("Serif", "B", BODY_SIZE_PT)
        self.set_text_color(31, 78, 121) if level == 2 else self.set_text_color(35, 55, 65)
        self.multi_cell(0, BODY_LINE_MM, text, align="L")
        self.set_text_color(0, 0, 0)
        self.ln(2 if level == 2 else 1)
        if level == 2:
            self.start_section(text, level=1)

    def add_paragraph(self, text: str):
        # The embedded Times subsets lack part of the Arabic alphabet. Arabic
        # therefore uses DejaVu Sans explicitly; Latin text uses Times New Roman.
        self.set_font("Sans" if self.arabic_mode else "Serif", "", BODY_SIZE_PT)
        align = "R" if self.arabic_mode else "J"
        self.multi_cell(0, BODY_LINE_MM, text, align=align, markdown=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)

    def add_bullet(self, text: str, ordered: str | None = None):
        self.set_font("Serif", "", BODY_SIZE_PT)
        prefix = f"{ordered}. " if ordered else "• "
        self.set_x(self.l_margin + 4)
        self.multi_cell(self.content_width - 4, BODY_LINE_MM, prefix + text, align="J", markdown=True,
                        new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)

    def add_callout(self, text: str):
        self.ensure_space(24)
        self.set_font("Serif", "B", BODY_SIZE_PT)
        self.set_fill_color(232, 241, 245)
        self.multi_cell(0, BODY_LINE_MM, text, align="J", fill=True, markdown=True,
                        padding=(2, 2, 2, 2), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2.5)

    def add_equation(self, text: str):
        self.ensure_space(18)
        self.set_font("Serif", "", BODY_SIZE_PT)
        self.multi_cell(0, BODY_LINE_MM, text, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)

    def add_source(self, text: str):
        self.set_font("Serif", "", 10)
        self.set_text_color(85, 85, 85)
        self.multi_cell(0, 5.5, "Source : " + text, align="R", wrapmode="WORD")
        self.set_text_color(0, 0, 0)
        self.ln(1.5)

    def add_reference(self, text: str):
        self.set_font("Serif", "", BODY_SIZE_PT)
        self.set_x(self.l_margin + 5)
        self.multi_cell(self.content_width - 5, BODY_LINE_MM, text, align="L", wrapmode="WORD",
                        new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1.8)

    def add_figure(self, asset: str, title: str):
        if not self.current_chapter:
            raise ValueError(f"Figure without chapter: {asset}")
        key = ("Figure", self.current_chapter)
        self.counts[key] += 1
        label = f"Figure {self.current_chapter}.{self.counts[key]}"
        path = ASSETS / "figures" / f"{asset}.png"
        if not path.exists():
            raise FileNotFoundError(path)
        with Image.open(path) as image:
            aspect = image.height / image.width
        width = min(160, self.content_width)
        height = width * aspect
        if height > 145:
            height = 145
            width = height / aspect
        self.ensure_space(height + 24)
        x = (self.w - width) / 2
        self.image(str(path), x=x, y=self.get_y(), w=width, h=height)
        self.set_y(self.get_y() + height + 3)
        self.set_font("Serif", "B", 10)
        self.multi_cell(0, 5.5, f"{label} — {title}", align="C")
        self.caption_pages[label] = self.page_no()
        self.ln(2)

    def add_table(self, rows: list[list[str]], caption: str | None, weights: str | None = None):
        if not rows:
            return
        # A preceding FPDF table or cell may leave the cursor at the right edge.
        # Reset before captions and before the next full-width table.
        self.set_x(self.l_margin)
        cols = len(rows[0])
        if any(len(row) != cols for row in rows):
            raise ValueError(f"Malformed table near {caption or rows[0]}")
        label = ""
        if caption:
            if not self.current_chapter:
                raise ValueError(f"Numbered table outside chapter: {caption}")
            key = ("Tableau", self.current_chapter)
            self.counts[key] += 1
            label = f"Tableau {self.current_chapter}.{self.counts[key]}"
            self.ensure_space(35)
            self.set_x(self.l_margin)
            self.set_font("Serif", "B", 10)
            self.multi_cell(0, 5.5, f"{label} — {caption}", align="C")
            self.caption_pages[label] = self.page_no()
            self.ln(1)
        # The unnumbered abbreviation index is a front-matter lookup table;
        # compact leading keeps its explanatory note off an otherwise empty page.
        compact_index = caption is None and self.current_part == "LISTE DES ABRÉVIATIONS"
        table_size = 8.1 if compact_index else 8.5
        table_leading = 4.2 if compact_index else 4.6
        self.set_font("Serif", "", table_size)
        self.set_x(self.l_margin)
        kwargs = {
            "rows": rows,
            "width": self.content_width,
            "borders_layout": "ALL",
            "line_height": table_leading,
            "padding": 0.8,
            "text_align": "L",
            "markdown": True,
            "headings_style": FontFace(family="Serif", emphasis="B", size_pt=table_size, color=(255, 255, 255), fill_color=(31, 78, 121)),
            "repeat_headings": 1,
        }
        if weights:
            values = [float(v) for v in weights.split(",")]
            if len(values) != cols:
                raise ValueError(f"Column weight mismatch for {label}: {weights}")
            kwargs["col_widths"] = tuple(values)
        with self.table(**kwargs):
            pass
        self.ln(3)

    def render_caption_list(self, kind: str, templates: list[CaptionTemplate], pages: int):
        for index in range(pages):
            self.add_content_page()
            if index == 0:
                self.set_font("Serif", "B", 14)
                self.multi_cell(0, 8, f"LISTE DES {kind.upper()}S", align="C")
                self.ln(5)
            subset = templates[index * 40:(index + 1) * 40]
            self.set_font("Serif", "", 8.8)
            for item in subset:
                page = self.previous_pages.get(item.label, 0)
                text = f"{item.label} — {item.title}"
                # Two-column borderless layout with a right-aligned page number.
                self.set_x(self.l_margin)
                self.multi_cell(self.content_width - 14, 4.6, text, align="L", wrapmode="WORD")
                self.set_xy(self.w - self.r_margin - 12, self.get_y() - 4.6)
                self.cell(12, 4.6, str(page) if page else "—", align="R")
                self.ln(5.2)

    def render_toc(self, outline):
        self.set_font("Serif", "", 9.2)
        for section in outline:
            if section.level > 1:
                continue
            self.set_x(self.l_margin + section.level * 6)
            if section.level == 0:
                self.set_font("Serif", "B", 9.2)
            else:
                self.set_font("Serif", "", 8.8)
            text = section.name
            width = self.content_width - section.level * 6 - 14
            self.multi_cell(width, 5, text, align="L")
            self.set_xy(self.w - self.r_margin - 12, self.get_y() - 5)
            self.cell(12, 5, str(section.page_number), align="R")
            self.ln(5.4)


def parse_table(lines: list[str], start: int) -> tuple[list[list[str]], int]:
    raw = []
    i = start
    while i < len(lines) and lines[i].strip().startswith("|"):
        raw.append(lines[i].strip())
        i += 1
    rows = []
    for index, line in enumerate(raw):
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if index == 1 and all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells):
            continue
        rows.append(cells)
    return rows, i


def render_markdown(pdf: ThesisPDF, text: str, body: bool = True):
    lines = text.splitlines()
    paragraph: list[str] = []
    pending_table: tuple[str, str | None] | None = None

    def flush():
        nonlocal paragraph
        if paragraph:
            value = " ".join(part.strip() for part in paragraph).strip()
            if value:
                if not body and pdf.arabic_mode:
                    pdf.add_paragraph(value)
                elif pdf.current_part.startswith("BIBLIOGRAPHIE"):
                    pdf.add_reference(value)
                else:
                    pdf.add_paragraph(value)
            paragraph = []

    i = 0
    while i < len(lines):
        raw = lines[i]
        line = raw.strip()
        if not line:
            flush()
            i += 1
            continue
        if line.startswith("|" ):
            flush()
            rows, i = parse_table(lines, i)
            caption, weights = pending_table or (None, None)
            pdf.add_table(rows, caption, weights)
            pending_table = None
            continue
        if line.startswith("# "):
            flush()
            pdf.add_major_heading(line[2:].strip(), toc=body)
        elif line.startswith("## "):
            flush()
            pdf.add_heading(line[3:].strip(), 2)
        elif line.startswith("### "):
            flush()
            pdf.add_heading(line[4:].strip(), 3)
        elif line.startswith("#### "):
            flush()
            pdf.add_heading(line[5:].strip(), 4)
        elif line == "[[PAGEBREAK]]":
            flush()
            pdf.add_content_page()
        else:
            fig = FIG_RE.match(line)
            tab = TABLE_RE.match(line)
            eq = EQ_RE.match(line)
            source = SOURCE_RE.match(line)
            ref = REF_RE.match(line)
            if fig:
                flush()
                pdf.add_figure(fig.group(1), fig.group(2).strip())
            elif tab:
                flush()
                pending_table = (tab.group(1).strip(), tab.group(2))
            elif eq:
                flush()
                pdf.add_equation(eq.group(1).strip())
            elif source:
                flush()
                pdf.add_source(source.group(1).strip())
            elif ref:
                flush()
                pdf.add_reference(ref.group(1).strip())
            elif line.startswith("> "):
                flush()
                pdf.add_callout(line[2:].strip())
            elif re.match(r"^[-*] ", line):
                flush()
                pdf.add_bullet(line[2:].strip())
            elif re.match(r"^\d+\. ", line):
                flush()
                match = re.match(r"^(\d+)\.\s+(.+)$", line)
                pdf.add_bullet(match.group(2), match.group(1))
            else:
                paragraph.append(line)
        i += 1
    flush()
    if pending_table:
        raise ValueError(f"Table caption without Markdown table: {pending_table[0]}")


def build(output: Path, previous_pages: dict[str, int] | None = None) -> tuple[ThesisPDF, ScanResult]:
    scan = scan_content()
    pdf = ThesisPDF(previous_pages)
    pdf.set_title("Particularités de la reconnaissance géotechnique des ponts — version révisée")
    pdf.set_author("BERKANE Dhiyaddine")
    pdf.set_subject("Étude bibliographique — version révisée et traçable")
    pdf.add_cover()
    render_markdown(pdf, read(CONTENT / "00_front.md"), body=False)
    # Reset language shaping after the Arabic abstract before French lists.
    pdf.set_rtl(False)
    figures = [item for item in scan.captions if item.kind == "Figure"]
    tables = [item for item in scan.captions if item.kind == "Tableau"]
    pdf.render_caption_list("Figure", figures, max(1, math.ceil(len(figures) / 40)))
    pdf.render_caption_list("Tableau", tables, max(1, math.ceil(len(tables) / 40)))
    render_markdown(pdf, read(CONTENT / "00_abbreviations.md"), body=False)
    pdf.add_content_page()
    pdf.set_font("Serif", "B", 14)
    pdf.multi_cell(0, 8, "TABLE DES MATIÈRES", align="C")
    pdf.ln(5)
    toc_pages = max(1, math.ceil(scan.outline_count / 43))
    pdf.insert_toc_placeholder(lambda doc, outline: doc.render_toc(outline), pages=toc_pages, allow_extra_pages=False)
    # The placeholder leaves the cursor on the first page after the reserved TOC.
    # Reuse it for the introduction instead of creating a blank intervening page.
    pdf.continue_current_page = True
    for filename in BODY_FILES:
        render_markdown(pdf, read(CONTENT / filename), body=True)
    pdf.output(str(output))
    return pdf, scan


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DELIVERABLES / "These_revisee_BERKANE_Dhiyaddine.pdf")
    parser.add_argument("--report", type=Path, default=ROOT / "audits" / "build_report.json")
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_suffix(".pass1.pdf")
    first, scan = build(temporary)
    second, _ = build(args.output, first.caption_pages)
    temporary.unlink(missing_ok=True)
    expected = {item.label for item in scan.captions}
    missing = sorted(expected - set(second.caption_pages))
    unexpected = sorted(set(second.caption_pages) - expected)
    caption_pages_stable = first.caption_pages == second.caption_pages
    page_count_stable = first.page_no() == second.page_no()
    report = {
        "output": str(args.output),
        "pages": second.page_no(),
        "outline_entries": scan.outline_count,
        "figures": len([c for c in scan.captions if c.kind == "Figure"]),
        "tables": len([c for c in scan.captions if c.kind == "Tableau"]),
        "missing_captions": missing,
        "unexpected_captions": unexpected,
        "caption_pages_stable_between_passes": caption_pages_stable,
        "page_count_stable_between_passes": page_count_stable,
        "caption_pages": second.caption_pages,
        "warnings": second.warnings,
        "formatting_profile": {
            "paper": "A4", "margins_mm": {"top": 25, "right": 25, "bottom": 25, "left": 25},
            "body_font": "Times New Roman", "body_size_pt": 12,
            "body_line_spacing": 1.5, "body_line_height_mm": BODY_LINE_MM,
            "chapter_titles": "Times New Roman 14 pt bold",
            "section_titles": "Times New Roman 12 pt bold",
            "figure_captions": "centered below, 10 pt", "table_captions": "centered above, 10 pt",
            "sources": "right aligned, 10 pt", "paragraph_alignment": "justified",
            "pagination": "continuous Arabic numerals, centered in footer",
            "glyph_fallback": "DejaVu Serif/Sans only for characters absent from the source Times subsets; Arabic abstract uses DejaVu Sans",
        },
        "times_new_roman_provenance": second.font_provenance,
    }
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "caption_pages"}, ensure_ascii=False, indent=2))
    if missing or unexpected or not caption_pages_stable or not page_count_stable:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
