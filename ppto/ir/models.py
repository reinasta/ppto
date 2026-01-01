from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Size:
    """Physical size of an element, in pixels at the document DPI."""

    width: float
    height: float


@dataclass
class Point:
    """Absolute top-left coordinate, in pixels at the document DPI."""

    x: float
    y: float


@dataclass
class Color:
    """RGB color encoded as a hex string (e.g., #RRGGBB)."""

    hex: str


@dataclass
class TextRun:
    text: str
    font_size_pt: Optional[float] = None
    color: Optional[Color] = None
    bold: Optional[bool] = None
    italic: Optional[bool] = None


@dataclass
class TextBox:
    position: Point
    size: Size
    runs: List[TextRun] = field(default_factory=list)
    fill_color: Optional[Color] = None
    z_index: int = 0


@dataclass
class ImageElement:
    position: Point
    size: Size
    source: str
    description: Optional[str] = None
    z_index: int = 0


@dataclass
class Background:
    color: Optional[Color] = None
    image: Optional[str] = None


@dataclass
class Slide:
    index: int
    background: Background = field(default_factory=Background)
    text_boxes: List[TextBox] = field(default_factory=list)
    images: List[ImageElement] = field(default_factory=list)


@dataclass
class Theme:
    colors: List[Color] = field(default_factory=list)


@dataclass
class Document:
    size: Size
    dpi: int
    theme: Theme = field(default_factory=Theme)
    slides: List[Slide] = field(default_factory=list)
