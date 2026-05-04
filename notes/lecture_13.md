---
title: Dynamic Stochastic General Equilibrium
short_title: Lecture 13
subtitle: Modeling Macroeconomics | Lecture 13
label: lecture-13
date: 2026-04-21
description: Stochastic dynamic general equilibrium foundations covering the Brock-Mirman closed-form stochastic growth model and the Prescott Real Business Cycle framework, with a focus on the hours volatility puzzle.
tags:
  - DSGE
  - Brock-Mirman
  - real business cycle
  - stochastic growth
  - hours volatility
  - calibration
---

## Materials

- [Slides: Dynamic Stochastic General Equilibrium](/slides/m13/dsge-slides.html)

## Notebooks

The following computational notebook accompanies the source chapters in the Reading Assignment below:

- [Dynamic Stochastic General Equilibrium: Brock-Mirman and the Prescott RBC Model](../notebooks/dsge.md): Companion to [The Brock-Mirman Stochastic Growth Model](https://jhu-econ.github.io/intertemporal-choice/content/dsge/BrockMirman/) and [The Prescott Real Business Cycle Model](https://jhu-econ.github.io/intertemporal-choice/content/dsge/RBC-Prescott/)

## Learning Objectives

By the end of this lecture, students will be able to:

1. Derive the closed-form consumption rule $\kappa = 1 - \alpha\beta$ in the Brock-Mirman model and identify the three knife-edge assumptions that make it possible
2. Explain why the expected-self steady state coincides with the no-shocks steady state in Brock-Mirman and why this coincidence is special to the linear-in-income consumption rule
3. Derive the log-linear law of motion $k_{t+1} = \log(\alpha\beta) + a_t + \alpha k_t$ and interpret the AR(1) coefficient as capital's share
4. Set up the Prescott RBC household problem with Cobb-Douglas preferences over consumption and leisure, and derive the intratemporal FOC $w\ell/c = \zeta/(1-\zeta)$
5. Calibrate the leisure weight $\zeta$ from long-run time-use data and explain why Cobb-Douglas is the unique preference class consistent with the lack of trend in hours
6. State the hours volatility puzzle, distinguish the two candidate mechanisms (labor supply elasticity vs interest rate channel), and explain why each fails to match the data

## Key Concepts

- **Brock-Mirman closed form**: with 100 percent depreciation, log utility, and Cobb-Douglas production, the consumption rule is linear in income with MPC $\kappa = 1 - \alpha\beta$ and the $A_{t+1}$ terms cancel exactly inside the Euler equation
- **Stochastic steady state**: three definitions (no-shocks limit, ergodic mean, expected-self point) coexist in the literature; they coincide in Brock-Mirman but generally differ in richer models, and the ergodic mean requires a stationary shock process to exist
- **Cobb-Douglas preferences over consumption and leisure**: $u(c, \ell) = (c^{1-\zeta}\ell^\zeta)^{1-\rho}/(1-\rho)$ is the unique class that keeps the budget share of leisure constant when wages change, consistent with the long-run facts documented by Ramey and Francis (2009)
- **Leisure weight calibration**: under the assumption $c \approx wn$, the intratemporal FOC implies $\ell = \zeta$, giving $\zeta \approx 2/3$ for a 40-hour work week with 8 hours of sleep per day
- **Leisure Euler equation**: $\widehat{\ell}_{t+1} \approx -\widehat{w}_{t+1} + (r_{t+1} - \theta)$ where $\theta \equiv -\log\beta$ is the time preference rate (distinct from depreciation $\delta$); hours respond to wage and interest rate movements
- **Hours volatility puzzle**: the RBC model matches $\sigma_y$ at 84 percent of the US data but under-predicts $\sigma_n$ by half; resolving the gap via a large labor supply elasticity contradicts micro evidence, and resolving it via the interest rate channel implies counterfactual consumption comovement
- **Calibration vs estimation**: Summers (1986) argues that Prescott's moment-matching procedure is a rhetorical exercise without standard errors or a formal rejection region; this methodological debate shapes the DSGE literature through to New Keynesian extensions

## Reading Assignment

:::{attention} Required Reading
Before Lecture 14, read the following chapters from [A Gentle Introduction to Intertemporal Choice](https://jhu-econ.github.io/intertemporal-choice/):

1. [The Brock-Mirman Stochastic Growth Model](https://jhu-econ.github.io/intertemporal-choice/content/dsge/BrockMirman/)
2. [The Prescott Real Business Cycle Model](https://jhu-econ.github.io/intertemporal-choice/content/dsge/RBC-Prescott/)
:::

## Final Project

:::{important} Group Project: Integrating DSGE with Macroeconomic Theory
The DSGE lecture launches the semester's capstone: a group research project that
extends one of four starter models and integrates it with another chapter of
the course. Deliverable is a single Jupyter notebook that contains both the
working code and the written report in interleaved markdown cells.

**Weight:** 25 percent of the final grade.
**Due:** 2026-05-05, 11:59 PM (Canvas).
**Groups:** Already assigned (three students per group).

**Starter notebooks** (pick one):

| Notebook | Model |
|----------|-------|
| `brock_mirman.ipynb` | Analytical stochastic growth with log utility and full depreciation |
| `rbc_prescott.ipynb` | Prescott RBC with labor-leisure and Blanchard-Kahn solution |
| `rck_discrete.ipynb` | Discrete-time Ramsey-Cass-Koopmans with CRRA utility and shooting |
| `diamond_olg.ipynb` | Stochastic overlapping generations with intergenerational risk |

**Integration requirement:** pair your starter with at least one other chapter:
consumption (CLO2), asset pricing (CLO3), investment (CLO4), or growth (CLO5).

**Project categories** (pick one):

- *Theoretical extensions*: add a new mechanism (habit formation, adjustment costs, equity premium, PAYG social security)
- *Empirical applications*: calibrate or estimate against FRED or long-run data
- *Policy analysis*: evaluate a specific policy question (investment tax credit, optimal capital taxation, Social Security reform)
- *Computational development*: implement VFI, projection methods, or Blanchard-Kahn on a starter that does not yet use them
:::

:::{attention} In-Class Presentation
On the last day of class, each group delivers a 10-minute presentation
followed by 5 minutes of Q&A. Motivate the question, summarize model and
methods without excessive derivation, show key figures, and discuss economic
interpretation. Slides are not required; you may present directly from your
computational notebook, from slides, or from any combination of the two.
:::

:::{note} Grading Weights
Rubric (100 points total): code and correctness (25), written analysis (25),
presentation (20), creativity and depth (20), notebook quality (10). Full
rubric and academic integrity policy on Canvas.
:::

:::{warning} Check your DataCamp grades now
If you have completed any DataCamp assignments that are still showing a zero
in the gradebook, email the instructor immediately. Ungraded completions that
are not flagged before the end of the semester will remain zeros.
:::

## Looking Ahead

:::{important} Week 14 (2026-04-28): Reading Week
Week 14 is a short online session in which the instructor presents one of his
own research papers, illustrating how the DSGE toolkit is applied in
practice. The rest of the week is reserved as reading time to prepare for
final presentations and the exam. No new chapter readings are assigned; use
the time to finish the final project and review post-midterm material.
:::

:::{important} Week 15 (2026-05-05): Presentations and Final Exam
The final session has two parts:

1. **Group presentations** (first half): each group delivers a 10-minute talk followed by 5 minutes of Q&A. Final project notebooks are also due by 11:59 PM on this date.
2. **Midterm 2** (second half): a short exam focused on material from *since Midterm 1*: investment theory, growth theory I and II, and DSGE (Lectures 10-13). Questions target post-midterm concepts, so earlier chapters will not be tested directly. The material itself is cumulative, though: asset pricing and growth build on the consumption foundations from the first half, and you are expected to bring that understanding with you.
:::

:::{tip} Course Materials
- Course website: [jhu-econ.github.io/moma](https://jhu-econ.github.io/moma)
- Textbook: [A Gentle Introduction to Intertemporal Choice](https://jhu-econ.github.io/intertemporal-choice/)
:::
