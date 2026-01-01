from pathlib import Path

from ppto import emit_latex, emit_typst
from ppto.ir import models


def build_document() -> models.Document:
    return models.Document(
        size=models.Size(width=960, height=540),
        dpi=96,
        slides=[
            models.Slide(
                index=1,
                background=models.Background(color=models.Color(hex="#112233")),
                text_boxes=[
                    models.TextBox(
                        position=models.Point(x=100, y=120),
                        size=models.Size(width=300, height=150),
                        runs=[
                            models.TextRun(
                                text="Title",
                                font_size_pt=20,
                                color=models.Color(hex="#222222"),
                                bold=True,
                            ),
                            models.TextRun(text="subtitle", italic=True),
                        ],
                        fill_color=models.Color(hex="#FFFFAA"),
                        z_index=2,
                    )
                ],
                images=[
                    models.ImageElement(
                        position=models.Point(x=20, y=30),
                        size=models.Size(width=200, height=100),
                        source="figure.png",
                        description="plot",
                        z_index=1,
                    )
                ],
            )
        ],
    )


def test_slide_to_latex_formats_content(tmp_path: Path) -> None:
    document = build_document()
    image_path = tmp_path / "slide-1.png"
    image_path.write_bytes(b"fake")

    latex = emit_latex.slide_to_latex(document.slides[0], document, image_path)

    assert rf"\usebackgroundtemplate{{\includegraphics[width=\paperwidth]{{{image_path.as_posix()}}}}}" in latex
    assert r"\begin{tikzpicture}[remember picture,overlay]" in latex
    assert r"\textbf{" in latex
    assert r"\textit{" in latex
    text_width_cm = f"{emit_latex._px_to_cm(document.slides[0].text_boxes[0].size.width, document.dpi):.2f}cm"  # type: ignore[attr-defined]
    assert f"text width={text_width_cm}" in latex
    image_width_cm = f"{emit_latex._px_to_cm(document.slides[0].images[0].size.width, document.dpi):.2f}cm"  # type: ignore[attr-defined]
    image_height_cm = f"{emit_latex._px_to_cm(document.slides[0].images[0].size.height, document.dpi):.2f}cm"  # type: ignore[attr-defined]
    assert f"width={image_width_cm}" in latex
    assert f"height={image_height_cm}" in latex


def test_slide_to_typst_formats_content(tmp_path: Path) -> None:
    document = build_document()
    image_path = tmp_path / "slide-1.png"
    image_path.write_bytes(b"fake")

    typst = emit_typst.slide_to_typst(document.slides[0], document, image_path)

    slide_width_cm = f"{emit_typst._px_to_cm(document.size.width, document.dpi):.2f}cm"  # type: ignore[attr-defined]
    slide_height_cm = f"{emit_typst._px_to_cm(document.size.height, document.dpi):.2f}cm"  # type: ignore[attr-defined]
    assert f'#image("{image_path.as_posix()}", width: {slide_width_cm}, height: {slide_height_cm}' in typst
    assert 'fill: "#222222"' in typst
    assert "size: 20pt" in typst
    text_dx = f"{emit_typst._px_to_cm(100, document.dpi):.2f}cm"  # type: ignore[attr-defined]
    text_dy = f"{emit_typst._px_to_cm(120, document.dpi):.2f}cm"  # type: ignore[attr-defined]
    assert f"#place(left + top, dx: {text_dx}, dy: {text_dy})" in typst
