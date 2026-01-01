from __future__ import annotations

from pathlib import Path
from typing import Iterable, List

from .ir import models


def _px_to_cm(px: float, dpi: int) -> float:
    return (px / dpi) * 2.54


def slide_to_typst(slide: models.Slide, document: models.Document, image_path: Path) -> str:
    width_cm = _px_to_cm(document.size.width, document.dpi)
    height_cm = _px_to_cm(document.size.height, document.dpi)
    lines: List[str] = []
    lines.append(f"#box(width: {width_cm:.2f}cm, height: {height_cm:.2f}cm)[")
    if slide.background.image or image_path:
        lines.append(
            f"  #place(top + left)[#image(\"{image_path.as_posix()}\", width: {width_cm:.2f}cm, height: {height_cm:.2f}cm, fit: \"cover\")]"
        )
    elif slide.background.color:
        lines.append(f"  #rect(width: {width_cm:.2f}cm, height: {height_cm:.2f}cm, fill: \"{slide.background.color.hex}\")")

    for text_box in sorted(slide.text_boxes, key=lambda t: t.z_index):
        x_cm = _px_to_cm(text_box.position.x, document.dpi)
        y_cm = _px_to_cm(text_box.position.y, document.dpi)
        w_cm = _px_to_cm(text_box.size.width, document.dpi)
        content_parts: List[str] = []
        for run in text_box.runs:
            style_parts: List[str] = []
            if run.font_size_pt:
                style_parts.append(f"size: {run.font_size_pt}pt")
            if run.color:
                style_parts.append(f"fill: \"{run.color.hex}\"")
            styled_text = run.text.replace("\n", " \\\\ ")
            if style_parts:
                content_parts.append(f"#text({', '.join(style_parts)})[{styled_text}]")
            else:
                content_parts.append(styled_text)
        text_body = " ".join(content_parts)
        lines.append(
            f"  #place(left + top, dx: {x_cm:.2f}cm, dy: {y_cm:.2f}cm)["
            f"#box(width: {w_cm:.2f}cm)[{text_body}]]"
        )

    for image in sorted(slide.images, key=lambda i: i.z_index):
        x_cm = _px_to_cm(image.position.x, document.dpi)
        y_cm = _px_to_cm(image.position.y, document.dpi)
        w_cm = _px_to_cm(image.size.width, document.dpi)
        h_cm = _px_to_cm(image.size.height, document.dpi)
        lines.append(
            f"  #place(left + top, dx: {x_cm:.2f}cm, dy: {y_cm:.2f}cm)["
            f"#image(\"{image.source}\", width: {w_cm:.2f}cm, height: {h_cm:.2f}cm, fit: \"cover\")]"
        )
    lines.append("]")
    return "\n".join(lines)


def emit(document: models.Document, out_dir: Path, images: Iterable[Path]) -> List[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    slide_paths: List[Path] = []
    for slide, image_path in zip(document.slides, images):
        slide_file = out_dir / f"slide-{slide.index}.typ"
        slide_file.write_text(slide_to_typst(slide, document, image_path), encoding="utf-8")
        slide_paths.append(slide_file)
    return slide_paths
