from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict

from . import models


def document_to_dict(document: models.Document) -> Dict[str, Any]:
    return asdict(document)


def document_to_json(document: models.Document, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document_to_dict(document), indent=2), encoding="utf-8")


def load_document(path: Path) -> models.Document:
    data = json.loads(path.read_text(encoding="utf-8"))
    return dict_to_document(data)


def dict_to_document(data: Dict[str, Any]) -> models.Document:
    def color(raw):
        return models.Color(hex=raw["hex"])

    def point(raw):
        return models.Point(x=raw["x"], y=raw["y"])

    def size(raw):
        return models.Size(width=raw["width"], height=raw["height"])

    def text_run(raw):
        return models.TextRun(
            text=raw["text"],
            font_size_pt=raw.get("font_size_pt"),
            color=color(raw["color"]) if raw.get("color") else None,
            bold=raw.get("bold"),
            italic=raw.get("italic"),
        )

    def text_box(raw):
        return models.TextBox(
            position=point(raw["position"]),
            size=size(raw["size"]),
            runs=[text_run(r) for r in raw.get("runs", [])],
            fill_color=color(raw["fill_color"]) if raw.get("fill_color") else None,
            z_index=raw.get("z_index", 0),
        )

    def image_el(raw):
        return models.ImageElement(
            position=point(raw["position"]),
            size=size(raw["size"]),
            source=raw["source"],
            description=raw.get("description"),
            z_index=raw.get("z_index", 0),
        )

    def background(raw):
        if not raw:
            return models.Background()
        return models.Background(
            color=color(raw["color"]) if raw.get("color") else None,
            image=raw.get("image"),
        )

    def slide(raw):
        return models.Slide(
            index=raw["index"],
            background=background(raw.get("background")),
            text_boxes=[text_box(t) for t in raw.get("text_boxes", [])],
            images=[image_el(i) for i in raw.get("images", [])],
        )

    theme = models.Theme(
        colors=[color(c) for c in data.get("theme", {}).get("colors", [])]
    )
    return models.Document(
        size=size(data["size"]),
        dpi=data["dpi"],
        theme=theme,
        slides=[slide(s) for s in data.get("slides", [])],
    )
