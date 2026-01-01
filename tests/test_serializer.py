from pathlib import Path

from ppto.ir import models, serializer


def sample_document() -> models.Document:
    return models.Document(
        size=models.Size(width=1280, height=720),
        dpi=150,
        theme=models.Theme(colors=[models.Color(hex="#AA0000")]),
        slides=[
            models.Slide(
                index=1,
                background=models.Background(color=models.Color(hex="#112233")),
                text_boxes=[
                    models.TextBox(
                        position=models.Point(x=50, y=75),
                        size=models.Size(width=400, height=200),
                        runs=[
                            models.TextRun(
                                text="Hello world",
                                font_size_pt=14,
                                color=models.Color(hex="#333333"),
                                bold=True,
                            ),
                            models.TextRun(text="Body text", italic=True),
                        ],
                        fill_color=models.Color(hex="#EEEEEE"),
                        z_index=1,
                    )
                ],
                images=[
                    models.ImageElement(
                        position=models.Point(x=10, y=20),
                        size=models.Size(width=300, height=250),
                        source="image.png",
                        description="example image",
                        z_index=0,
                    )
                ],
            )
        ],
    )


def test_document_round_trip(tmp_path: Path) -> None:
    document = sample_document()
    ir_path = tmp_path / "ir.json"

    serializer.document_to_json(document, ir_path)
    loaded = serializer.load_document(ir_path)

    assert loaded == document
    assert loaded.slides[0].background.color == models.Color(hex="#112233")
    assert loaded.slides[0].text_boxes[0].runs[0].color == models.Color(hex="#333333")
