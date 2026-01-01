# ppto

Prototype PPTX exporter with CLI helpers for Beamer and Typst.

Install dependencies:

```
pip install -r requirements.txt
```

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
