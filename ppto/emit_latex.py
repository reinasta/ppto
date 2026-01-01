from __future__ import annotations

from pathlib import Path
from typing import Iterable, List

from .ir import models


def _px_to_cm(px: float, dpi: int) -> float:
    return (px / dpi) * 2.54


def slide_to_latex(slide: models.Slide, document: models.Document, image_path: Path) -> str:
    width_cm = _px_to_cm(document.size.width, document.dpi)
    height_cm = _px_to_cm(document.size.height, document.dpi)
    lines: List[str] = []
    lines.append(r"\begin{frame}")
    if slide.background.image or image_path:
        image_str = image_path.as_posix()
        lines.append(
            rf"\usebackgroundtemplate{{\includegraphics[width=\paperwidth]{{{image_str}}}}}"
        )
    elif slide.background.color:
        lines.append(
            rf"\usebackgroundtemplate{{\color{{{slide.background.color.hex}}}\rule{{\paperwidth}}{{\paperheight}}}}"
        )
    lines.append(r"\begin{tikzpicture}[remember picture,overlay]")
    for text_box in sorted(slide.text_boxes, key=lambda t: t.z_index):
        x_cm = _px_to_cm(text_box.position.x, document.dpi)
        y_cm = _px_to_cm(text_box.position.y, document.dpi)
        w_cm = _px_to_cm(text_box.size.width, document.dpi)
        color_prefix = ""
        if text_box.fill_color:
            color_prefix = rf"\colorbox{{{text_box.fill_color.hex}}}{{"
        text_content = ""
        for run in text_box.runs:
            content = run.text.replace("\n", r"\\")
            style_prefix = ""
            if run.font_size_pt:
                style_prefix += rf"\fontsize{{{run.font_size_pt}}}{{{run.font_size_pt*1.2}}}\selectfont "
            if run.color:
                style_prefix += rf"\textcolor{{{run.color.hex}}}{{"
                content += "}"
            if run.bold:
                style_prefix += r"\textbf{"
                content += "}"
            if run.italic:
                style_prefix += r"\textit{"
                content += "}"
            text_content += style_prefix + content
        node = (
            rf"\node[anchor=north west,text width={w_cm:.2f}cm] at "
            rf"($(current page.north west)+({x_cm:.2f}cm,-{y_cm:.2f}cm)$)"
            rf" {{{color_prefix}{text_content}{'{' if color_prefix else ''}}};"
        )
        lines.append(node)
    for image in sorted(slide.images, key=lambda i: i.z_index):
        x_cm = _px_to_cm(image.position.x, document.dpi)
        y_cm = _px_to_cm(image.position.y, document.dpi)
        w_cm = _px_to_cm(image.size.width, document.dpi)
        h_cm = _px_to_cm(image.size.height, document.dpi)
        lines.append(
            rf"\node[anchor=north west] at "
            rf"($(current page.north west)+({x_cm:.2f}cm,-{y_cm:.2f}cm)$)"
            rf" {{\includegraphics[width={w_cm:.2f}cm,height={h_cm:.2f}cm,keepaspectratio]{{{image.source}}}}};"
        )
    lines.append(r"\end{tikzpicture}")
    lines.append(r"\end{frame}")
    return "\n".join(lines)


def emit(document: models.Document, out_dir: Path, images: Iterable[Path]) -> List[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    slide_paths: List[Path] = []
    for slide, image_path in zip(document.slides, images):
        slide_file = out_dir / f"slide-{slide.index}.tex"
        slide_file.write_text(slide_to_latex(slide, document, image_path), encoding="utf-8")
        slide_paths.append(slide_file)
    return slide_paths
