# ppto

Prototype PPTX exporter with CLI helpers for Beamer and Typst.

## Setup with `uv`

This project now uses [`uv`](https://github.com/astral-sh/uv) for dependency management. To create a virtual environment with all runtime and development dependencies:

```
uv sync --dev
```

Run the CLI through `uv` to ensure the environment is active:

```
uv run ppto convert slides.pptx --target latex --out out/
```

> If you prefer `pip`, a `requirements.txt` is provided for convenience.

## Usage

Render slides to PNGs and LaTeX snippets:

```
ppto convert slides.pptx --target latex --out out/
```

Export IR only:

```
ppto convert slides.pptx --mode ir --out out/
```

Emit Typst snippets from a saved IR:

```
ppto emit --ir out/ir.json --target typst --out out/typst/
```
