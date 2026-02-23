---
title: Slides
---

Lecture slides are posted here each week. Each module covers a different topic in macroeconomic modeling.

- [M01: Foundations of Scientific Computing](/slides/m01/foundations-scientific-computing-slides.html)
- M02: Snow day (no class)
- [M03: Intertemporal Choice](/slides/m03/intertemporal-choice-slides.html)
- [M04: Consumption Theory](/slides/m04/consumption-theory-slides.html)
- [M05: Advanced Consumption Models](/slides/m05/advanced-consumption-slides.html)
- [M06: Risk and Consumption](/slides/m06/risk-and-consumption-slides.html)

## Building Slides Locally

Slides are built with [Quarto](https://quarto.dev/). To build or preview slides on your own computer:

### 1. Install Quarto

Download and install Quarto from [quarto.dev/docs/get-started](https://quarto.dev/docs/get-started/).

Alternatively, use a package manager:

```bash
# macOS (Homebrew)
brew install quarto

# Windows (Chocolatey)
choco install quarto

# Linux (Debian/Ubuntu) - download .deb from quarto.dev
sudo dpkg -i quarto-*.deb
```

Verify the installation:

```bash
quarto --version
```

### 2. Preview Slides

From the project root directory:

```bash
uv run quarto preview slides/m03/intertemporal-choice-slides.qmd
```

This opens a live preview in your browser that updates as you edit.

### 3. Build All Slides

To build all slides to HTML:

```bash
uv run quarto render slides/
```

The output files are placed alongside the source `.qmd` files.
