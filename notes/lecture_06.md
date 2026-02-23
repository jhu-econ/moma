---
title: Risk and Consumption
short_title: Lecture 06
subtitle: Modeling Macroeconomics | Lecture 06
label: lecture-06
date: 2025-02-24
description: How risk affects consumption decisions under CRRA and CARA preferences, including precautionary saving with risky returns, closed-form solutions under CARA utility with income uncertainty, and the Campbell-Mankiw decomposition of consumption dynamics with time-varying interest rates.
tags:
  - consumption
  - precautionary saving
  - CRRA
  - CARA
  - Campbell-Mankiw
  - time-varying interest rates
---

## Materials

- [Slides: Risk and Consumption](/slides/m06/risk-and-consumption-slides.html)

## Notebooks

The following computational notebook is a companion to the reading assigned in [Lecture 05](./lecture_05.md):

- [Risk and Consumption](../notebooks/risk_and_consumption.md): Companion to [Consumption out of Risky Assets](https://jhu-econ.github.io/intertemporal-choice/content/consumption/crra-raterisk/), [Consumption with CARA Utility](https://jhu-econ.github.io/intertemporal-choice/content/consumption/caramodelwithyrisk/), and [Dynamics of Consumption with Time-Varying R](https://jhu-econ.github.io/intertemporal-choice/content/consumption/campmancrrawithtimevaryingr/)

## Learning Objectives

By the end of this lecture, students will be able to:

1. Apply the guess-and-verify method to derive the exact MPC out of risky wealth under CRRA utility with lognormal returns
2. Decompose the approximate MPC into income, substitution, and precautionary saving components
3. Explain why log utility ($\rho = 1$) is a knife-edge case where risk does not affect the consumption level
4. Derive the closed-form consumption process under CARA utility with normally distributed permanent income shocks
5. Identify the precautionary premium in the CARA model and explain why it is independent of wealth
6. Describe the three channels through which interest rates affect consumption in the CARA framework (income, substitution, human wealth)
7. Use the Campbell-Mankiw log-linearization to express the consumption-wealth ratio as a function of expected future interest rates
8. Explain when income effects dominate substitution effects based on the intertemporal elasticity of substitution

## Key Concepts

- **Guess-and-verify method**: Postulating a linear consumption rule $c_t = \kappa\,m_t$ and showing it satisfies the Euler equation; works when market resources cancel but fails when labor income enters
- **Precautionary saving (CRRA)**: The $-(\rho - 1)\sigma_r^2/2$ term in the approximate MPC formula; consumers with $\rho > 1$ save more as return risk increases
- **CARA utility**: Constant absolute risk aversion $u(C) = -(1/\alpha)e^{-\alpha C}$; produces additive rather than multiplicative consumption changes, and the precautionary premium $\alpha\sigma_\Psi^2/2$ does not depend on wealth
- **Precautionary premium**: The additional expected consumption growth under uncertainty relative to perfect foresight; reflects the extra saving needed to self-insure against income shocks
- **Campbell-Mankiw decomposition**: Log-linearization of the budget constraint that expresses the consumption-wealth ratio as a discounted sum of future interest rates minus consumption growth
- **Income vs. substitution effects**: The coefficient $(1 - \rho^{-1})$ governs the net response of consumption to interest rate changes; when $\rho > 1$ the income effect dominates
- **Human wealth effect**: Interest rate changes alter the present value of future labor income $H_t \approx Y_t/(r-g)$, a channel that can dominate the direct income and substitution effects

## Reading Assignment

:::{attention} Required Reading
Before Lecture 07, read the following chapters from [A Gentle Introduction to Intertemporal Choice](https://jhu-econ.github.io/intertemporal-choice/):

1. [Risk and Prudence and Precautionary Premia](https://jhu-econ.github.io/intertemporal-choice/content/consumption/riskandpspremia/)
2. [The Consumption Function](https://jhu-econ.github.io/intertemporal-choice/content/consumption/consumptionfunction/)
3. [Buffer Stock Consumption](https://jhu-econ.github.io/intertemporal-choice/content/consumption/bufferstockageprofiles/)

These readings move from analytical precautionary saving results to the numerical consumption function and its buffer-stock properties.
:::

## Homework

:::{attention} Assignment 2: Computational Notebook
A computational notebook covering all consumption modules to date. Details will be provided in class.

**Due:** Check Canvas for the deadline.
:::

:::{attention} Assignment: DataCamp
Complete the next DataCamp assignment posted on Canvas.

**Due:** Check Canvas for the deadline.
:::

:::{note}
If you are behind on previous DataCamp assignments, you may still complete them for credit. See [Lecture 01](./lecture_01.md), [Lecture 02](./lecture_02.md), [Lecture 03](./lecture_03.md), [Lecture 04](./lecture_04.md), and [Lecture 05](./lecture_05.md) for the earlier assignments.
:::

:::{tip} Course Materials
- Course website: [jhu-econ.github.io/moma](https://jhu-econ.github.io/moma)
- Textbook: [A Gentle Introduction to Intertemporal Choice](https://jhu-econ.github.io/intertemporal-choice/)
:::
