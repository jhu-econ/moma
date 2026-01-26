---
title: Development Environment Setup
short_title: Lecture 01
subtitle: Modeling Macroeconomics | Lecture 01
label: lecture-01
date: 2025-01-20
description: Set up GitHub, VS Code, uv, and Jupyter for Modeling Macroeconomics.
tags:
  - setup
  - tools
  - Python
---

## Materials

- [Slides: Foundations of Scientific Computing](/slides/m01/foundations-scientific-computing-slides.html)

## Learning Objectives

By the end of this lecture, students will be able to:

1. Create and configure a GitHub account
2. Install and configure VS Code with Python extensions
3. Install the `uv` package manager on their operating system
4. Initialize a Python project with `uv`
5. Add scientific computing packages to their project
6. Run Python scripts and Jupyter notebooks

## Prerequisites

:::{important}
Before class, ensure you have:
- A computer running Windows, macOS, or Linux
- Internet connection
- Administrative access to install software
:::

## Part 1: GitHub Account Setup

### Why GitHub?

GitHub provides version control and collaboration tools essential for modern computational work. We will use it to:

- Submit assignments
- Track changes to your code
- Collaborate on projects
- Build a portfolio of your work

### Creating an Account

1. Navigate to [github.com](https://github.com)
2. Click "Sign up"
3. Use your JHU email address for educational benefits
4. Choose a professional username (this will be visible to future employers)
5. Complete email verification

### GitHub Student Developer Pack

:::{tip} Free Benefits for Students
GitHub offers valuable benefits through the Student Developer Pack:

- GitHub Pro (unlimited private repositories, advanced tools)
- Free domain names
- Cloud credits (Azure, AWS, DigitalOcean)
- Developer tools and learning resources

Apply at [education.github.com/pack](https://education.github.com/pack) using your JHU email.
:::

### Installing GitHub Desktop

GitHub Desktop provides a graphical interface for Git, making version control more accessible.

1. Download from [desktop.github.com](https://desktop.github.com)
2. Install and sign in with your GitHub account
3. Grant permissions when prompted

GitHub Desktop handles authentication automatically, so you won't need to configure SSH keys or tokens.

### Configuring Git (Optional)

:::{note}
:class: dropdown
**For command-line users:** If you prefer using Git from the terminal, configure your identity:

```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@jhu.edu"
```

This step is optional if you're using GitHub Desktop exclusively.
:::

## Part 2: Installing VS Code

Visual Studio Code is a free, powerful code editor with excellent support for Python, Jupyter notebooks, and MyST Markdown.

### Download and Install

1. Download from [code.visualstudio.com](https://code.visualstudio.com)
2. Run the installer for your operating system
3. Launch VS Code after installation

### Recommended Extensions

Install these extensions from the Extensions sidebar ({kbd}`Ctrl+Shift+X` / {kbd}`Cmd+Shift+X`):

:::{list-table} Required Extensions
:header-rows: 1

* - Extension
  - Purpose
* - **Python**
  - Python language support, debugging, and IntelliSense
* - **Jupyter**
  - Run and edit Jupyter notebooks inside VS Code
* - **MyST-Markdown**
  - Syntax highlighting for MyST documents
:::

To install an extension, search for its name and click **Install**.

## Part 3: Installing uv

`uv` is a fast Python package and project manager written in Rust. It replaces pip, virtualenv, and pyenv with a single tool.

### Windows Installation

Open PowerShell and run:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

:::{warning}
You must restart your terminal after installation for `uv` to be available in your PATH.
:::

### macOS Installation

Open Terminal and run:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

:::{hint}
:class: dropdown
**Homebrew alternative:** If you use Homebrew, you can install with `brew install uv` instead.
:::

### Linux Installation

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Verifying Installation

Confirm `uv` is installed correctly:

```bash
uv --version
```

:::{seealso}
For more information, visit the [uv documentation](https://docs.astral.sh/uv/).
:::

## Part 4: Creating Your First Project

### Directory Structure

We will use a consistent directory structure throughout the course. Create a `github` folder in your home directory to store all your repositories:

**macOS/Linux:**
```bash
mkdir -p ~/github
cd ~/github
```

**Windows (PowerShell):**
```powershell
mkdir ~\github
cd ~\github
```

:::{hint}
The `~` symbol refers to your home directory:
- **macOS:** `/Users/yourname`
- **Windows:** `C:\Users\yourname`
- **Linux:** `/home/yourname`
:::

### Initialize a New Project

Create your course repository folder and initialize it:

```bash
mkdir moma
cd moma
uv init
```

Your full path will be `~/github/moma`, which will later sync with your GitHub repository online.

This creates:
- `pyproject.toml` — project configuration and dependencies
- `.python-version` — specifies the Python version
- `main.py` — a sample Python file
- `README.md` — project documentation
- `.gitignore` — files to exclude from version control

### Project Structure

```
~/github/
└── moma/
    ├── .gitignore
    ├── .python-version
    ├── README.md
    ├── main.py
    └── pyproject.toml
```

## Part 5: Adding Dependencies

### Course Packages

Add the packages we will use throughout the course:

```bash
uv add numpy scipy matplotlib mystmd jupyter
```

This installs:
- `numpy` — numerical arrays and linear algebra
- `scipy` — optimization, integration, and scientific routines
- `matplotlib` — plotting and visualization
- `mystmd` — MyST Markdown for writing and publishing documents
- `jupyter` — interactive notebooks (includes JupyterLab, Notebook, and related tools)

### Verify Installation

Test that packages are available:

```bash
uv run python -c "import numpy; import scipy; import matplotlib; print('Success!')"
```

Verify MyST is installed:

```bash
uv run myst --version
```

:::{caution}
If you see `ModuleNotFoundError`, make sure you're in the `~/github/moma` directory and that `uv add` completed successfully.
:::

## Part 6: Running Python Code

### Using uv run

Execute Python scripts within the project environment:

```bash
uv run python main.py
```

### Interactive Python

Start an interactive session:

```bash
uv run python
```

### JupyterLab

Launch JupyterLab for interactive notebook computing:

```bash
uv run jupyter lab
```

This opens a browser window with the JupyterLab interface. You can also open notebooks directly in VS Code using the Jupyter extension.

### Quick Test

In VS Code, create a new file `test_setup.py` in your `moma` folder:

```{code-block} python
:filename: test_setup.py
:linenos:

import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt

# Simple optimization example
f = lambda x: (x - 2)**2
result = opt.minimize_scalar(f)
print(f"Minimum at x = {result.x:.4f}")

# Plot
x = np.linspace(0, 4, 100)
plt.plot(x, f(x))
plt.xlabel("x")
plt.ylabel("f(x)")
plt.title("Quadratic Function")
plt.savefig("test_plot.png")
print("Plot saved to test_plot.png")
```

Run it:

```bash
uv run python test_setup.py
```

:::{tip}
If successful, you'll see `Minimum at x = 2.0000` and a new `test_plot.png` file in your folder.
:::

## Summary

:::{note} What We Covered
1. **GitHub** — account creation, Student Developer Pack, and GitHub Desktop
2. **VS Code** — installation and recommended extensions
3. **uv** — installation on Windows, macOS, and Linux
4. **Project initialization** — `uv init` creates a new project
5. **Dependencies** — `uv add` installs packages
6. **Running code** — `uv run` for scripts, JupyterLab for notebooks
:::

## Homework

:::{attention} Assignment 1: Repository Setup
Publish your local `~/github/moma` folder to GitHub:

1. In GitHub Desktop, select **File > Add Local Repository**
2. Navigate to `~/github/moma` (or `~\github\moma` on Windows) and click **Add Repository**
3. Click **Publish repository** in the top bar
4. Uncheck "Keep this code private" if you want your work to be public
5. Click **Publish Repository** to create the remote repository on GitHub
6. Submit your repository URL on Canvas

**Due:** Before Lecture 2
:::

:::{tip} Course Materials
The course website at [jhu-econ.github.io/moma](https://jhu-econ.github.io/moma) contains all lecture notes and materials. Your personal `moma` repository is your workspace for assignments and experimentation.
:::

:::{seealso} Additional Resources
- [GitHub Docs](https://docs.github.com) — Official GitHub documentation
- [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial) — Getting started with Python in VS Code
- [uv Documentation](https://docs.astral.sh/uv/) — Complete uv reference
- [MyST Markdown Guide](https://mystmd.org/guide) — Writing scientific documents
:::
