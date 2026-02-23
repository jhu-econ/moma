---
title: Notebooks
description: >-
  Computational notebooks accompanying the lecture slides, covering
  two-period consumption, labor supply, the envelope condition,
  perfect foresight CRRA, the consumption random walk, the permanent
  income hypothesis, the Diamond OLG model, habit formation, durable
  goods, and quasi-hyperbolic discounting.
keywords:
  - computational economics
  - Python
  - Euler equation
  - OLG
  - consumption
tags:
  - notebooks
---

# Notebooks

This directory contains MyST Markdown computational notebooks that serve as companions to the lecture slides. Each notebook provides detailed derivations, Python implementations, and exercises.

## Contents

| File | Topic |
|------|-------|
| `consumption_two_period.md` | The Fisher two-period consumption problem, CRRA utility, Fisherian separation, and the labor supply puzzle |
| `olg_extra.md` | The Diamond OLG model: competitive equilibrium, social planner, Golden Rule, and dynamic efficiency |
| `envelope_crra.md` | The envelope condition, multiperiod Euler equation, and the perfect foresight CRRA consumption model |
| `random_walk_cons_fn.md` | Hall's random walk proposition, the permanent income hypothesis, and MPCs out of permanent vs transitory shocks |
| `advanced_consumption.md` | Habit formation, durable goods, and quasi-hyperbolic discounting (Laibson) |
| `risk_and_consumption.md` | CRRA with risky returns, CARA with income risk, and Campbell-Mankiw time-varying interest rates |

## Libraries

The notebooks demonstrate the use of:

- **NumPy** for numerical computation
- **SciPy** for optimization (root-finding with `brentq`)
- **Matplotlib** for visualization
- **SymPy** for symbolic derivations
- **pandas** for tabular summaries

## Running the Notebooks

See the [Getting Started](../README.md#getting-started) section in the root README for initial setup.

To build the notebooks:

```bash
uv run myst build --execute
```

To run interactively in JupyterLab:

```bash
uv run jupyter lab
```

Then right-click any `.md` file and select **Open With > Notebook**.
