---
title: HANK Research and Final Exam Prep
short_title: Lecture 14
subtitle: Modeling Macroeconomics | Lecture 14
label: lecture-14
date: 2026-04-28
description: Reading-week session combining a research seminar on Heterogeneous Agent New Keynesian (HANK) models, a cumulative study guide for Midterm 2 covering Lectures 10 through 13, and the format of the final project presentation.
tags:
  - HANK
  - heterogeneous agents
  - DSGE
  - study guide
  - final project
  - presentations
---

## Materials

- [Slides: Investment Theory](/slides/m10/investment-theory-slides.html)
- [Slides: Growth Theory I](/slides/m11/growth-theory-slides.html)
- [Slides: Growth Theory II](/slides/m12/endogenous-growth-slides.html)
- [Slides: Dynamic Stochastic General Equilibrium](/slides/m13/dsge-slides.html)

This is a short reading-week session with three parts: a research seminar by the instructor on Heterogeneous Agent New Keynesian (HANK) models, a cumulative study guide for Midterm 2, and the format of next week's final project presentations.

---

## Research Seminar: HANK Models

The instructor presented current research on **Heterogeneous Agent New Keynesian (HANK)** models, illustrating how the DSGE toolkit developed in Lecture 13 extends to environments with realistic household heterogeneity.

### Why HANK

The representative-agent New Keynesian (RANK) workhorse, a direct descendant of Brock-Mirman and Prescott, ignores cross-sectional differences in wealth, MPC, and income risk. Three empirical observations push the literature toward heterogeneity:

- The MPC out of transitory income is **0.05** in the representative-agent benchmark but is closer to **0.25 to 0.50** in the data, with most of the action coming from low-wealth households (a fact the consumption block of the course emphasized in Lectures 4 to 6).
- Monetary policy transmits through **indirect** channels (labor income response of constrained households) far more than through the **direct** channel (intertemporal substitution by unconstrained savers) that RANK relies on.
- Fiscal multipliers, the consumption response to government spending, and the distribution of welfare gains depend on *who* receives the shock, which RANK cannot speak to by construction.

### How HANK Builds on the Course

HANK is not a new framework so much as a fusion of three pieces students already know:

| Course block | What HANK builds on |
|---|---|
| Consumption under uncertainty (Lectures 4 to 6) | Precautionary saving, buffer-stock behavior, MPC heterogeneity. HANK formalizes these in incomplete-markets economies in the Bewley-Aiyagari-Huggett tradition (not covered in this course) |
| Asset pricing (Lecture 7) | The stochastic discount factor, now indexed by household type |
| DSGE (Lecture 13) | The aggregate Euler equation and the labor-leisure FOC. HANK then layers on the New Keynesian frictions (Calvo or Rotemberg sticky prices, sticky wages) that M13 only previewed |

The new ingredient is the **distribution of household wealth** as an aggregate state, which HANK tracks with computational methods (sequence-space Jacobian, perturbation around the steady-state distribution) rather than with the closed-form algebra that made Brock-Mirman tractable.

### Pedagogical Takeaway

HANK shows where the techniques of this course go next: same Euler equation, same first-order conditions, but with a non-trivial cross-section that resolves several puzzles the representative-agent benchmark cannot. The research presented in class is one application of this toolkit; further work in the area is referenced in the slides distributed during the seminar.

---

## Midterm 2 Study Guide

Midterm 2 is the second half of next week's session and covers material from since Midterm 1: investment theory (Lecture 10), growth theory I and II (Lectures 11 and 12), and DSGE (Lecture 13). Earlier chapters are not tested directly, although the consumption foundations remain in the background.

This study guide focuses on the key concepts, results, and equations from Lectures 10 through 13. Derivations are summarized; focus on understanding what each result says and when it applies.

---

### Investment Theory (Lecture 10)

#### Why Investment Matters

- Investment averages roughly 15 to 20\% of GDP, but its standard deviation is several times larger than that of consumption or GDP itself ($\sigma(I)/\sigma(Y) \approx 4$ in postwar US data)
- A small share of the level can still account for a large share of the variance, so investment fluctuations drive a disproportionate part of business-cycle variation in output
- This empirical fact motivates building a richer theory of investment than the static Hall-Jorgenson benchmark

#### The Hall-Jorgenson Cost of Capital

- A static neoclassical firm rents capital at rental rate $\kappa_t^{\text{rent}}$ and produces $y = k^\alpha$
- The first-order condition pins down the optimal capital stock: $k^* = \alpha y / \kappa_t^{\text{rent}}$
- The **no-arbitrage condition** between deposits and physical capital, combined with corporate tax $\tau$ and investment tax credit $\zeta$, gives the **effective cost of capital**:

$$c_k = \frac{(r + \delta)(1 - \zeta)}{1 - \tau}\,p_k$$

- An ITC lowers $c_k$ and raises $k^*$; a corporate tax raises $c_k$ and lowers $k^*$
- The model is a theory of the *level* of capital, not investment dynamics: capital adjusts instantly

#### Tobin's Q

- $Q \equiv \text{stock-market value} / \text{replacement cost}$
- Investment rule: expand when $Q > 1$, contract when $Q < 1$
- Intuition: when the market values an installed unit at more than its replacement cost, building one more raises shareholder value
- Average $Q$ is observable; this is what makes the rule empirically testable

#### The Abel-Hayashi Marginal $q$ Model

- Convex adjustment costs $j(i_t, k_t)$ penalize rapid changes in capital
- The Euler equation for investment links the shadow price of capital (**marginal $q$**) to the marginal cost of investing
- Investment is a smooth, increasing function of $q_t$, generating gradual capital accumulation consistent with the data
- **Hayashi's theorem (1982):** under perfect capital markets, constant returns to scale, and price-taking firms, marginal $q$ equals average $Q$

#### Capital Market Imperfections

- When external funds are more expensive than internal funds, Hayashi's theorem fails
- Investment then responds to current cash flow even after controlling for $Q$
- Empirically (Fazzari-Hubbard-Petersen 1988), cash-flow sensitivity is largest for plausibly constrained firms; this is the standard interpretation of the violation of $q$-theory

---

### Growth Theory I: Ramsey-Cass-Koopmans (Lecture 11)

#### The Keynes-Ramsey Rule

- The social planner maximizes $\int_0^\infty u(c_t) e^{-\vartheta t} dt$ subject to $\dot k = f(k) - c - (n + g + \delta) k$ in efficiency units
- The Hamiltonian first-order conditions give the **Keynes-Ramsey rule**:

$$\frac{\dot c}{c} = \frac{1}{\rho}\!\left[f'(k) - (n + \delta) - \vartheta - \rho g\right]$$

- This is the same Euler equation as in the perfect-foresight consumption model, except $f'(k)$ is now endogenous

#### Steady State and Golden Rule

- Setting $\dot c / c = 0$:

$$f'(\check k) = \vartheta + n + \delta + \rho g$$

- The **golden rule** maximizes per-capita consumption in steady state and satisfies $f'(k^{GR}) = n + g + \delta$
- In the standard case, $\check k < k^{GR}$ because impatience ($\vartheta > 0$) makes the planner unwilling to forgo current consumption for the larger long-run consumption that more capital would allow

#### Phase Diagram and the Saddle Path

- Two loci in the $(k, c)$ plane: $\dot k = 0$ (an inverted-$U$) and $\dot c = 0$ (a vertical line at $\check k$)
- Through any $k_0$, only the **saddle path** converges to the steady state
- Off-saddle trajectories either drive $c \to 0$ in finite time or violate the transversality condition

#### Decentralization

- Without externalities or distortions, the competitive equilibrium replicates the planner's allocation (First Welfare Theorem)
- Failures of the FWT include externalities (Lecture 12), distortionary taxes, and capital-market frictions

#### Ricardian Equivalence

- With infinite horizons and lump-sum taxes, the *timing* of taxation does not matter; only the present value of government spending does
- A tax cut today financed by a future tax is fully saved; consumption is unchanged

#### Capital Income Tax

- A capital income tax distorts the after-tax return on saving:

$$f'(\check k)(1 - \tau_k) = \vartheta + n + \rho g + \delta$$

- The steady-state capital stock falls
- A lump-sum rebate restores income but not the price of future consumption, so the distortion remains

---

### Growth Theory II: Endogenous Growth (Lecture 12)

#### Why Growth Cannot Be Endogenized Trivially

- Under perfect competition with constant returns to scale, **Euler's theorem** gives $Y = F_K K + F_L L$
- Factor payments exhaust output, leaving no resources for the fixed costs of producing knowledge
- Endogenous growth requires departing from one of the three: perfect competition, constant returns at the firm level, or diminishing returns to accumulated factors

#### The Rebelo AK Model

- Production $Y = AK$ with constant marginal product $A$
- Growth rate of consumption (with $n = 0$): $\dot c / c = \rho^{-1}(A - \delta - \vartheta)$
- **No transitional dynamics, no convergence:** identical-parameter countries with different starting capital stocks grow in parallel forever

#### The Romer (1986) Knowledge Externality

- Each firm produces $y_j = k_j^\alpha \ell_j^{1-\alpha} \Xi^\eta$ with aggregate knowledge $\Xi$ taken as given
- In equilibrium $\Xi = K$; with $\eta = 1 - \alpha$ the model exhibits constant returns to capital at the aggregate level
- **Wedge:** the private firm internalizes only $\alpha$ as the marginal product, while the planner internalizes the full $\alpha + \eta = 1$
- Decentralized growth $\rho^{-1}(\alpha - \vartheta)$ falls below the planner's $\rho^{-1}(1 - \vartheta)$
- Capital accumulation should be subsidized

#### The Lucas (1988) Human Capital Model

- Human capital accumulates via schooling time: $\dot h / h = \phi(1 - u)$
- Without an externality, planner and decentralized growth both equal $\rho^{-1}(\phi - \vartheta)$
- With a positive human-capital externality $\bar h^\psi$ and standard $\rho > 1$, decentralized growth falls below the planner's, justifying education subsidies
- Defining **broad capital** $\bar k \equiv k^\alpha h^{1-\alpha}$ (the textbook writes this as $\kappa$; we use $\bar k$ here to avoid clash with the MPC notation) shows the model has the same AK structure as Rebelo

#### The Blanchard (1985) Perpetual-Youth Model

- Each consumer faces a constant probability $p$ of death per period
- The aggregate consumption function loads on the **effective discount rate** $\vartheta + p$
- **Ricardian equivalence fails:** a tax cut today financed by future taxes redistributes wealth from the unborn to the currently alive
- Aggregate capital is below the RCK level

#### The q-Ramsey Model

- Adds quadratic adjustment costs to the RCK framework
- Convergence to the steady state slows; both higher adjustment costs and higher risk aversion reduce convergence speed in similar ways
- The steady-state capital stock is unchanged

---

### DSGE (Lecture 13)

#### The Brock-Mirman Closed Form

- The model admits a **linear consumption rule** $c_t = (1 - \alpha\beta)\,y_t$ where $y_t = z_t k_t^\alpha$
- This relies on **three knife-edge assumptions**:
  - **100\% depreciation:** so $k_{t+1} = y_t - c_t$ exactly
  - **Cobb-Douglas production:** so $\alpha Y/K$ is the marginal product
  - **Log utility ($\rho = 1$):** so marginal utility ratios are $C_t/C_{t+1}$
- Together, these make the productivity shock $z_{t+1}$ cancel inside the Euler equation
- **MPC** $\kappa = 1 - \alpha\beta$, independent of $z_t$

#### Log-Linear Capital Dynamics

- Substituting the consumption rule into the capital equation gives the **AR(1) law of motion** in logs:

$$k_{t+1} = \log(\alpha\beta) + a_t + \alpha k_t$$

- The persistence parameter $\alpha$ is exactly capital's output elasticity; mean reversion is governed by diminishing returns

#### The Prescott Real Business Cycle Model

- Adds labor-leisure choice with **Cobb-Douglas preferences** $u(c, \ell) = (c^{1-\zeta}\ell^\zeta)^{1-\rho}/(1-\rho)$
- Cobb-Douglas is the unique class consistent with the long-run flatness of hours despite a century of trend wage growth
- **Intratemporal FOC:** $w_t \ell_t / c_t = \zeta/(1-\zeta)$
- Calibrating to a 40-hour work week against 112 waking hours per week gives $\ell \approx 2/3$ and $\zeta \approx 2/3$
- At this calibration, $w \ell / c = (2/3)/(1/3) = 2$: the **shadow value of leisure** is twice the value of consumption. Leisure is the dominant time-use category in dollar terms, so even small wage movements have large income effects, which is what makes the model's hours response large in principle

#### The Hours Volatility Puzzle

- The model matches output volatility (about 84\% of the US standard deviation)
- The model **under-predicts hours volatility by roughly half**
- Two candidate resolutions both fail:
  - **High Frisch elasticity:** RBC needs a Frisch elasticity of 2 or larger; micro evidence places it at 0.2 to 0.5
  - **Interest rate channel:** matching hours through intertemporal substitution requires interest rate movements that imply much larger consumption growth volatility than the data display
- The puzzle motivated the New Keynesian DSGE program, which preserves the Euler equation but adds frictions on prices, wages, and credit

---

## Final Project Presentation

The final project is due next week. The first half of the Week 15 session is reserved for in-class presentations.

### Format

- **Each group delivers a 10-minute presentation** followed by **5 minutes of Q&A**
- **Slides are not required.** You may present directly from your computational notebook (the same notebook you submit), from slides, or from any combination of the two
- The notebook deliverable (combined code and written report) is due the same day at 11:59 PM on Canvas

### Grading Reminder

The full project rubric (100 points: code 25, written analysis 25, presentation 20, creativity 20, notebook quality 10) is on Canvas. The presentation block alone is worth 20 of those 100 points.

---

## Looking Ahead

:::{important} Week 15 (2026-05-05): Final Session
The final session has two parts:

1. **Group presentations** (first half): each group delivers a 10-minute talk followed by 5 minutes of Q&A. Final project notebooks are also due by 11:59 PM on this date.
2. **Midterm 2** (second half): a short exam covering investment, growth I and II, and DSGE (Lectures 10 through 13). Format: 20 multiple choice (3 points each, 60 points total) and 3 free response (40 points total). 60 minutes.
:::

:::{tip} Reading Week
No new chapter readings are assigned. Use the time to finish the final project, prepare your presentation, and review the post-midterm material above. The slides for Lectures 10 through 13 are linked at the top of this page; the textbook chapters are linked from each lecture's notes.
:::

:::{warning} Final DataCamp Check
This is your last chance to flag any DataCamp completions that are not yet posted to the gradebook. Email the instructor before the end of the week.
:::

:::{tip} Course Materials
- Course website: [jhu-econ.github.io/moma](https://jhu-econ.github.io/moma)
- Textbook: [A Gentle Introduction to Intertemporal Choice](https://jhu-econ.github.io/intertemporal-choice/)
:::
