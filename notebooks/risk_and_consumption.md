---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
authors:
  - name: Alan Lujan
    url: https://github.com/alanlujan91
description: >-
  Risk and consumption: CRRA utility with risky asset returns (exact and
  approximate MPC), CARA utility with income uncertainty (precautionary
  premium and closed-form consumption function), and the Campbell-Mankiw
  decomposition of consumption dynamics with time-varying interest rates.
keywords:
  - CRRA
  - CARA
  - precautionary saving
  - Campbell-Mankiw
  - time-varying interest rates
  - lognormal returns
tags:
  - consumption
  - intertemporal-choice
---

# Risk and Consumption

How does risk affect consumption decisions? Part I derives the exact marginal propensity to consume for a CRRA consumer whose only asset has a risky return. The lognormal distributional assumption yields a closed-form MPC, and a Taylor approximation decomposes it into income, substitution, and precautionary saving components. Part II switches to CARA utility with normally distributed income shocks, producing a tractable model where precautionary saving is additive and independent of wealth. Part III introduces time-varying interest rates into a CRRA framework and derives the Campbell-Mankiw decomposition ({cite:t}`cmModel`) relating the consumption-wealth ratio to expected future returns.

::::{seealso}
This notebook builds on the envelope theorem and Euler equation machinery developed in [](./envelope_crra.md) and the random walk result from [](./random_walk_cons_fn.md). The precautionary saving motive studied here contrasts with the certainty-equivalence of quadratic utility, where risk does not affect optimal consumption.
::::

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import pandas as pd
from collections import namedtuple
```

```{code-cell} ipython3
# Parameters for the CRRA risky-return model
CRRARiskModel = namedtuple(
    'CRRARiskModel',
    ['beta', 'rho', 'r_tilde', 'sigma_r']
)

# Parameters for the CARA income-risk model
CARAModel = namedtuple(
    'CARAModel',
    ['R', 'beta', 'alpha', 'sigma_psi', 'Gamma', 'T']
)

# Parameters for the Campbell-Mankiw model
CampbellMankiwModel = namedtuple(
    'CampbellMankiwModel',
    ['beta', 'rho', 'xi', 'r_bar']
)
```

# Part I: CRRA with Risky Returns

A consumer with CRRA utility $u(c) = c^{1-\rho}/(1-\rho)$ holds a single risky asset. The return factor $\tilde{R}_{t+1}$ is lognormally distributed:

$$
\log \tilde{R}_{t+1} \sim \mathcal{N}\!\left(\tilde{r} - \sigma_r^2/2,\; \sigma_r^2\right),
$$

which ensures that $\mathbb{E}[\tilde{R}_{t+1}] = e^{\tilde{r}}$. The dynamic budget constraint is $m_{t+1} = (m_t - c_t)\tilde{R}_{t+1}$, where $m_t$ denotes market resources and no labor income enters.

## Guess-and-Verify for the MPC

The Euler equation is

```{math}
:label: crra_risk_euler
1 = \beta\,\mathbb{E}_t\!\left[\tilde{R}_{t+1}\left(\frac{c_{t+1}}{c_t}\right)^{-\rho}\right].
```

Postulate a consumption rule $c_t = \kappa\,m_t$, where $\kappa$ is a constant MPC. Substituting $c_{t+1} = \kappa\,m_{t+1} = \kappa(1-\kappa)m_t\,\tilde{R}_{t+1}$ into [](#crra_risk_euler), the $m_t$ terms cancel (they appear in both numerator and denominator raised to the same power). After simplification:

```{math}
:label: crra_risk_mpc
\kappa = 1 - \left(\beta\,\mathbb{E}_t[\tilde{R}_{t+1}^{1-\rho}]\right)^{1/\rho}.
```

This is an exact, closed-form result. The guess-and-verify approach works because market resources are the only source of wealth. If labor income appeared in the budget constraint, $m_t$ would not cancel and a linear consumption rule would fail.

```{code-cell} ipython3
#| output: asis
# Symbolic derivation of the exact MPC
from sympy.printing.mathml import mathml

def show(expr):
    ml = mathml(expr, printer='presentation')
    print(f'<math display="block" xmlns="http://www.w3.org/1998/Math/MathML">{ml}</math>')

beta_s, rho_s, sig_s, r_s = sp.symbols('beta rho sigma_r r', positive=True)
kappa_s = sp.Symbol('kappa')

# E[R^(1-rho)] for lognormal R
E_R_1_rho = sp.exp((1 - rho_s) * r_s - rho_s * (1 - rho_s) * sig_s**2 / 2)

# Exact MPC
mpc_exact = 1 - (beta_s * E_R_1_rho)**(1/rho_s)
mpc_exact_simplified = sp.simplify(mpc_exact)

print("**Lognormal expectation** $\\mathbb{E}[\\tilde{R}^{1-\\rho}]$:")
print()
show(E_R_1_rho)
print()
print("**Exact MPC:**")
print()
show(sp.Eq(kappa_s, mpc_exact_simplified))
```

## Evaluating the Lognormal Expectation

Since $\tilde{R}^{1-\rho}$ is also lognormally distributed with $\log \tilde{R}^{1-\rho} = (1-\rho)\log \tilde{R}$, the standard lognormal moment formula yields

```{math}
:label: crra_risk_elognorm
\mathbb{E}_t[\tilde{R}_{t+1}^{1-\rho}] = \exp\!\left[(1-\rho)\tilde{r} - \rho(1-\rho)\sigma_r^2/2\right].
```

The simplification involves collecting terms: $(1-\rho)^2\sigma_r^2/2$ from the lognormal formula combines with $-(1-\rho)\sigma_r^2/2$ from the mean specification to produce $-\rho(1-\rho)\sigma_r^2/2$.

## The Approximate MPC

Applying Taylor approximations ($\beta^{1/\rho} \approx \exp(-\rho^{-1}\vartheta)$ where $\beta = 1/(1+\vartheta)$) to the exact formula gives

```{math}
:label: crra_risk_approx
\kappa \approx \tilde{r} - \rho^{-1}(\tilde{r} - \vartheta) - (\rho - 1)\sigma_r^2/2.
```

Three terms correspond to three economic forces:

1. **Income effect** ($\tilde{r}$): higher returns generate more income, raising consumption
2. **Substitution effect** ($-\rho^{-1}(\tilde{r} - \vartheta)$): higher returns make future consumption cheaper, encouraging saving
3. **Precautionary saving** ($-(\rho-1)\sigma_r^2/2$): greater risk lowers the MPC (more saving) for $\rho > 1$

When $\sigma_r^2 = 0$, the formula reduces to the perfect foresight result $\kappa = \tilde{r} - \rho^{-1}(\tilde{r} - \vartheta)$.

```{code-cell} ipython3
# Compare exact and approximate MPC formulas
def exact_mpc(rho, r_tilde, sigma_r, beta):
    """Exact MPC for CRRA consumer with lognormal risky return."""
    E_R = np.exp((1 - rho) * r_tilde - rho * (1 - rho) * sigma_r**2 / 2)
    return 1 - (beta * E_R)**(1 / rho)

def approx_mpc(rho, r_tilde, sigma_r, vartheta):
    """Approximate MPC from Taylor expansion."""
    return r_tilde - (r_tilde - vartheta) / rho - (rho - 1) * sigma_r**2 / 2

params = CRRARiskModel(beta=1/1.04, rho=3.0, r_tilde=0.04, sigma_r=0.15)
vartheta = 1/params.beta - 1

rho_grid = np.linspace(1.01, 8.0, 200)
fig, axes = plt.subplots(1, 2, figsize=(10, 4))

# Panel 1: MPC vs risk aversion
mpc_ex = [exact_mpc(rho, params.r_tilde, params.sigma_r, params.beta) for rho in rho_grid]
mpc_ap = [approx_mpc(rho, params.r_tilde, params.sigma_r, vartheta) for rho in rho_grid]
axes[0].plot(rho_grid, mpc_ex, lw=2, label='Exact')
axes[0].plot(rho_grid, mpc_ap, '--', lw=2, label='Approximation')
axes[0].set_xlabel(r'Relative risk aversion $\rho$')
axes[0].set_ylabel(r'MPC $\kappa$')
axes[0].set_title(r'MPC falls as risk aversion rises ($\sigma_r = 0.15$)')
axes[0].legend(frameon=False, fontsize=8)
axes[0].grid(True, alpha=0.3)

# Panel 2: MPC vs return volatility
sig_grid = np.linspace(0, 0.30, 200)
mpc_ex_sig = [exact_mpc(params.rho, params.r_tilde, s, params.beta) for s in sig_grid]
mpc_ap_sig = [approx_mpc(params.rho, params.r_tilde, s, vartheta) for s in sig_grid]
axes[1].plot(sig_grid, mpc_ex_sig, lw=2, label='Exact')
axes[1].plot(sig_grid, mpc_ap_sig, '--', lw=2, label='Approximation')
axes[1].set_xlabel(r'Return volatility $\sigma_r$')
axes[1].set_ylabel(r'MPC $\kappa$')
axes[1].set_title(r'MPC falls as risk rises ($\rho = 3$)')
axes[1].legend(frameon=False, fontsize=8)
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

The left panel shows that more risk-averse consumers save more (lower MPC). The right panel shows the precautionary saving motive: as return volatility increases, the MPC falls. The approximation tracks the exact formula closely for moderate parameter values but diverges at extreme risk aversion or volatility.

```{code-cell} ipython3
# Tabulate the decomposition of the approximate MPC
rows = []
for rho in [1.0, 2.0, 3.0, 5.0]:
    income = params.r_tilde
    substitution = -(params.r_tilde - vartheta) / rho
    precautionary = -(rho - 1) * params.sigma_r**2 / 2
    total = income + substitution + precautionary
    exact = exact_mpc(rho, params.r_tilde, params.sigma_r, params.beta)
    rows.append({
        'rho': rho,
        'Income': round(income, 4),
        'Substitution': round(substitution, 4),
        'Precautionary': round(precautionary, 4),
        'Approx MPC': round(total, 4),
        'Exact MPC': round(exact, 4),
    })
df_decomp = pd.DataFrame(rows)
df_decomp
```

The table confirms that the precautionary term vanishes at $\rho = 1$ (log utility) and grows in magnitude with risk aversion. For $\rho = 5$, the precautionary component is $-0.045$, a substantial reduction in the MPC driven entirely by risk.

:::{note}
With log utility ($\rho = 1$), a mean-preserving spread in the return has no effect on consumption. The reason is subtle: the covariance between $\tilde{R}_{t+1}$ and $u'(c_{t+1})$ in the Euler equation $u'(c_t) = \beta\,\mathbb{E}_t[\tilde{R}_{t+1}\,u'(c_{t+1})]$ exactly offsets the Jensen's inequality effect. This makes log utility implausibly insensitive to risk; $\rho \geq 2$ is a more plausible lower bound.
:::

# Part II: CARA with Income Risk

## The Problem

A consumer with CARA utility $u(C) = -(1/\alpha)\,e^{-\alpha C}$ (where $\alpha > 0$ is the coefficient of absolute risk aversion) maximizes

```{math}
:label: cara_objective
\max \;\mathbb{E}_t\!\left[\sum_{s=t}^{T} \beta^{s-t}\,u(C_s)\right]
```

subject to $M_{t+1} = (M_t - C_t)R + Y_{t+1}$, where the interest rate $r = R - 1$ is constant. Income has two components: a deterministic trend $\bar{P}_{t+1} = \Gamma\bar{P}_t$ and a random-walk deviation $P_{t+1} = P_t + \Psi_{t+1}$, with $\Psi_{t+1} \sim \mathcal{N}(0, \sigma_\Psi^2)$.

## Perfect Foresight: Additive Growth

Under CARA, the Euler equation implies *additive* consumption changes:

```{math}
:label: cara_pf_growth
C_{t+1} = C_t + \alpha^{-1}\log(R\beta).
```

This contrasts sharply with CRRA, where consumption changes are *multiplicative* (affecting the growth rate). Under CARA, the intertemporal elasticity of substitution $\alpha^{-1}$ determines the absolute dollar increment in consumption per period.

```{code-cell} ipython3
#| output: asis
# Symbolic derivation of the CARA Euler equation
alpha_s, R_sym, beta_sym = sp.symbols('alpha R beta', positive=True)
C_t, C_t1 = sp.symbols('C_t C_{t+1}')

# u'(C) = exp(-alpha*C)
# Euler: u'(C_t) = R*beta*u'(C_{t+1})
# exp(-alpha*C_t) = R*beta*exp(-alpha*C_{t+1})
# -alpha*C_t = log(R*beta) - alpha*C_{t+1}
# C_{t+1} - C_t = (1/alpha)*log(R*beta)

growth = sp.Eq(C_t1 - C_t, sp.log(R_sym * beta_sym) / alpha_s)
print("**Perfect foresight Euler equation under CARA utility:**")
print()
show(growth)
print()
print("Consumption changes by a *constant dollar amount* each period, not a constant *rate*.")
```

## Solution Under Uncertainty

With normally distributed permanent income shocks, the consumption process

```{math}
:label: cara_solution
C_{t+1} = C_t + \alpha^{-1}\log(R\beta) + \alpha\sigma_\Psi^2/2 + \Psi_{t+1}
```

satisfies the Euler equation under uncertainty. To verify, substitute [](#cara_solution) into $1 = R\beta\,\mathbb{E}_t[\exp(-\alpha(C_{t+1} - C_t))]$ and use the fact that for $Z \sim \mathcal{N}(\mu, \sigma^2)$, $\mathbb{E}[e^Z] = e^{\mu + \sigma^2/2}$:

```{math}
:label: cara_verification
\begin{aligned}
1 &= R\beta\,\exp(-\alpha^2\sigma_\Psi^2/2)\,\exp(\alpha^2\sigma_\Psi^2/2)\,\exp(-\log R\beta) \\
&= R\beta \cdot (R\beta)^{-1} = 1. \quad \checkmark
\end{aligned}
```

```{code-cell} ipython3
#| output: asis
# Symbolic verification of the CARA solution under uncertainty
sigma_s = sp.Symbol('sigma_Psi', positive=True)
Psi_s = sp.Symbol('Psi_{t+1}')

delta_C = sp.log(R_sym * beta_sym) / alpha_s + alpha_s * sigma_s**2 / 2 + Psi_s
exp_neg_alpha_dC = sp.exp(-alpha_s * delta_C)

# Taking expectations: E[exp(-alpha*Psi)] = exp(alpha^2*sigma^2/2)
# so exp(-alpha*delta_C) without the shock part:
deterministic = sp.exp(-alpha_s * (sp.log(R_sym * beta_sym) / alpha_s + alpha_s * sigma_s**2 / 2))
shock_expect = sp.exp(alpha_s**2 * sigma_s**2 / 2)  # E[exp(-alpha*Psi)]

product = sp.simplify(R_sym * beta_sym * deterministic * shock_expect)

print("**Verification:** $R\\beta \\cdot \\exp(-\\alpha \\cdot \\text{det. part}) \\cdot \\mathbb{E}[\\exp(-\\alpha\\Psi)] =$")
print()
show(product)
```

## The Precautionary Premium

Define $\hat{\kappa} = \alpha^{-1}\log(R\beta) + \alpha\sigma_\Psi^2/2$. The consumption process becomes $C_{t+1} = C_t + \hat{\kappa} + \Psi_{t+1}$. The term $\alpha\sigma_\Psi^2/2$ is the **precautionary premium** ({cite:t}`caballero:jme`): it makes expected consumption growth faster than under certainty, reflecting additional saving today to buffer against future income risk. Two properties distinguish it from the CRRA case:

1. The premium is **additive** (a constant dollar amount per period), not multiplicative
2. It does **not depend on wealth** or income level, because CARA risk attitudes are constant in absolute terms

```{code-cell} ipython3
# Visualize the precautionary premium
params_cara = CARAModel(R=1.04, beta=0.96, alpha=2.0, sigma_psi=0.05, Gamma=1.02, T=60)

fig, axes = plt.subplots(1, 2, figsize=(10, 4))

# Panel 1: Consumption paths under different sigma
np.random.seed(42)
sigma_vals = [0.0, 0.03, 0.06, 0.10]
for sig in sigma_vals:
    khat = np.log(params_cara.R * params_cara.beta) / params_cara.alpha + params_cara.alpha * sig**2 / 2
    C = np.zeros(params_cara.T)
    C[0] = 10.0
    for t in range(1, params_cara.T):
        noise = np.random.normal(0, sig) if sig > 0 else 0.0
        C[t] = C[t-1] + khat + noise
    axes[0].plot(C, lw=1.5, label=rf'$\sigma_\Psi = {sig}$')

axes[0].set_xlabel('Period')
axes[0].set_ylabel('Consumption $C_t$')
axes[0].set_title('Higher uncertainty raises the consumption path (precautionary saving)')
axes[0].legend(frameon=False, fontsize=8)
axes[0].grid(True, alpha=0.3)

# Panel 2: Precautionary premium as function of sigma and alpha
sig_range = np.linspace(0, 0.12, 100)
for a in [1.0, 2.0, 4.0]:
    premium = a * sig_range**2 / 2
    axes[1].plot(sig_range, premium, lw=2, label=rf'$\alpha = {a}$')

axes[1].set_xlabel(r'Income volatility $\sigma_\Psi$')
axes[1].set_ylabel(r'Precautionary premium $\alpha\sigma_\Psi^2/2$')
axes[1].set_title('Premium is quadratic in volatility, linear in risk aversion')
axes[1].legend(frameon=False, fontsize=8)
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

```{code-cell} ipython3
# Table: precautionary premium for different combinations
rows = []
for a in [0.5, 1.0, 2.0, 4.0]:
    row = {'ARA (alpha)': a}
    for sig in [0.02, 0.05, 0.10]:
        row[f'sigma={sig}'] = round(a * sig**2 / 2, 6)
    rows.append(row)

df_premium = pd.DataFrame(rows)
df_premium.columns = [r'ARA ($\alpha$)'] + [rf'$\sigma_\Psi = {s}$' for s in [0.02, 0.05, 0.10]]
df_premium
```

## The Consumption Function

Imposing the intertemporal budget constraint, the infinite-horizon CARA consumption function is

```{math}
:label: cara_cons_fn
C_t = P_t + \frac{r}{R}\!\left[B_t + \frac{\bar{P}_t}{1 - \Gamma/R}\right] - r\!\left(\frac{\alpha^{-1}\log(R\beta) + \alpha\sigma_\Psi^2/2}{(1 - R)^2}\right),
```

where $P_t$ is the idiosyncratic permanent income level, $B_t$ is beginning-of-period bank balances, and $\bar{P}_t$ is the deterministic income trend.

Two notable features:

1. **The MPC out of capital is $r/R$**, the interest income on an extra dollar. It does not depend on impatience or risk aversion.
2. **The precautionary saving amount is independent of wealth.** The dollar amount saved for precautionary reasons is the same whether the consumer is rich or poor.

```{code-cell} ipython3
# Visualize the CARA consumption function: C vs B for different sigma
r = params_cara.R - 1
P_bar, P_level = 1.0, 0.0
B_grid = np.linspace(0, 20, 200)

fig, axes = plt.subplots(1, 2, figsize=(10, 4))

for sig in [0.0, 0.05, 0.10]:
    khat = np.log(params_cara.R * params_cara.beta) / params_cara.alpha + params_cara.alpha * sig**2 / 2
    human_wealth = P_bar / (1 - params_cara.Gamma / params_cara.R)
    precaut_term = r * khat / (1 - params_cara.R)**2
    C = P_level + (r / params_cara.R) * (B_grid + human_wealth) - precaut_term
    axes[0].plot(B_grid, C, lw=2, label=rf'$\sigma_\Psi = {sig}$')

axes[0].plot(B_grid, r / params_cara.R * B_grid + P_bar, 'k--', lw=1, alpha=0.5, label='Interest income')
axes[0].set_xlabel(r'Bank balances $B_t$')
axes[0].set_ylabel(r'Consumption $C_t$')
axes[0].set_title('CARA consumption function: parallel shifts with risk')
axes[0].legend(frameon=False, fontsize=8)
axes[0].grid(True, alpha=0.3)

# Panel 2: MPC out of bank balances is constant r/R
axes[1].plot(B_grid, np.full_like(B_grid, r / params_cara.R), color='C0', lw=2)
axes[1].set_xlabel(r'Bank balances $B_t$')
axes[1].set_ylabel(r'MPC $\partial C / \partial B$')
axes[1].set_xlim(0, 20)
axes[1].set_ylim(0, 0.08)
axes[1].set_title(f'MPC out of capital is constant: $r/R = {r/params_cara.R:.4f}$')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

The consumption function shifts down in parallel as income risk increases. The slope $\partial C / \partial B = r/R$ is identical across all risk levels, confirming that the MPC out of capital does not depend on uncertainty.

## Patience and Impatience

The infinite-horizon consumption function can be written as $C_t = \frac{R - (R\beta)^{1/\alpha}}{R}\,W_t$, where $W_t = B_t + H_t$ is total wealth. The consumer is **impatient** (spending more than income) when $(R\beta)^{1/\alpha} < 1$, and **patient** when $(R\beta)^{1/\alpha} > 1$. When $R\beta = 1$, the consumer spends exactly the interest income on total wealth: $C_t = (r/R)\,W_t$.

```{code-cell} ipython3
# MPC out of total wealth as function of R*beta for different alpha
Rbeta_grid = np.linspace(0.90, 1.10, 200)
fig, ax = plt.subplots(figsize=(8, 4))

for a in [1.0, 2.0, 5.0]:
    coeff = (params_cara.R - Rbeta_grid**(1/a)) / params_cara.R
    ax.plot(Rbeta_grid, coeff, lw=2, label=rf'$\alpha = {a}$')

ax.axhline(r / params_cara.R, color='gray', ls='--', lw=0.8, label=r'$r/R$ (balanced)')
ax.axvline(1.0, color='gray', ls='--', lw=0.8)
ax.set_xlabel(r'$R\beta$')
ax.set_ylabel('MPC out of total wealth')
ax.set_title('Impatient ($R\\beta < 1$): MPC exceeds $r/R$')
ax.legend(frameon=False, fontsize=8)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

## The Three Effects of $r$

Using the approximation $C_t \approx (r - \alpha^{-1}(r - \vartheta))[B_t + \bar{Y}R/r]$ (where $\vartheta = 1/\beta - 1$ is the time preference rate), three channels connect the interest rate to consumption:

1. **Income effect** (first $r$): higher $r$ increases the payout rate on total wealth
2. **Substitution effect** ($\alpha^{-1}(r - \vartheta)$): higher $r$ makes future consumption cheaper
3. **Human wealth effect** ($\bar{Y}R/r$ in the brackets): higher $r$ reduces the present value of future labor income

```{code-cell} ipython3
# Decompose the three effects of r on consumption
Y_bar = 1.0  # constant income
tau = 1/params_cara.beta - 1  # time preference rate
alpha_val = params_cara.alpha

r_grid = np.linspace(0.01, 0.10, 200)
R_grid = 1 + r_grid

fig, ax = plt.subplots(figsize=(8, 4))

# Total consumption at each r
B_val = 5.0
for a in [1.0, 2.0, 5.0]:
    C_approx = (r_grid - (r_grid - tau) / a) * (B_val + Y_bar * R_grid / r_grid)
    ax.plot(r_grid * 100, C_approx, lw=2, label=rf'$\alpha = {a}$')

ax.set_xlabel('Interest rate $r$ (%)')
ax.set_ylabel('Consumption $C_t$')
ax.set_title(f'Consumption vs. interest rate ($B = {B_val}$, $\\bar{{Y}} = {Y_bar}$)')
ax.legend(frameon=False, fontsize=8)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

# Part III: Consumption with Time-Varying Interest Rates

## The Campbell-Mankiw Framework

An infinite-horizon representative agent holds total wealth $W_t$ (human plus nonhuman). The return factor $R_{t+1}$ is riskless but varies over time:

```{math}
:label: cm_dbc
W_{t+1} = (W_t - C_t)\,R_{t+1}.
```

The goal is to express the consumption-wealth ratio as a function of expected future interest rates, separating income and substitution effects ({cite:t}`cmModel`).

## Log-Linearized Budget Constraint

Dividing [](#cm_dbc) by $W_t$, taking logs, and applying a Taylor expansion around the steady-state log consumption-wealth ratio $\bar{x} = \bar{c} - \bar{w}$:

```{math}
:label: cm_loglin
\Delta w_{t+1} \approx k + r_{t+1} + (1 - 1/\xi)(c_t - w_t),
```

where $\xi = 1 - \exp(\bar{x})$ is a constant slightly below one (since the consumption-wealth ratio $C/W$ is small), $k$ is a constant that depends on $\xi$, and lowercase letters denote logs.

## Forward Iteration

Setting two expressions for $\Delta w_{t+1}$ equal and iterating forward produces the **approximate intertemporal budget constraint**:

```{math}
:label: cm_approx_ibc
c_t - w_t = \sum_{j=1}^{\infty} \xi^j(r_{t+j} - \Delta c_{t+j}) + \frac{\xi k}{1 - \xi}.
```

This result is pure accounting: it holds for any consumption path consistent with the budget constraint. The log consumption-wealth ratio today must equal the discounted value of future returns minus future consumption growth. Higher expected future returns (holding consumption growth fixed) require higher consumption today.

```{code-cell} ipython3
#| output: asis
# Show the geometric sum structure symbolically
xi_s, r_s_sym, dc_s = sp.symbols('xi r_{t+j} Delta_c_{t+j}', positive=True)
j_s = sp.Symbol('j', positive=True, integer=True)

sum_expr = sp.Sum(xi_s**j_s * (r_s_sym - dc_s), (j_s, 1, sp.oo))
print("**Approximate IBC** (geometric discounting at rate $\\xi$):")
print()
print("$c_t - w_t =$")
show(sum_expr)
print()
print(r"$+ \;\xi k/(1-\xi)$")
```

## Substituting the Euler Equation

For a CRRA consumer with $u(c) = c^{1-\rho}/(1-\rho)$, the log Euler equation under perfect foresight is

$$
\Delta c_{t+1} = \mu + \rho^{-1} r_{t+1},
$$

where $\mu = \rho^{-1}\log\beta$. Substituting into [](#cm_approx_ibc) and collecting terms:

```{math}
:label: cm_cw_ratio
c_t - w_t = (1 - \rho^{-1})\sum_{j=1}^{\infty}\xi^j\,r_{t+j} + \frac{\xi(k - \mu)}{1-\xi}.
```

The coefficient $(1 - \rho^{-1})$ on expected future returns governs the net effect of interest rate changes on the consumption-wealth ratio.

```{code-cell} ipython3
# Impulse response of consumption-wealth ratio to interest rate shocks
params_cm = CampbellMankiwModel(beta=0.96, rho=3.0, xi=0.97, r_bar=0.04)

rho_vals = [0.5, 1.0, 2.0, 5.0]
T_irf = 40

fig, axes = plt.subplots(1, 2, figsize=(10, 4))

# Panel 1: Response to a persistent interest rate shock (phi = 0.8)
phi = 0.8
for rho in rho_vals:
    coeff = 1 - 1/rho
    r_shock = np.array([0.01 * phi**j for j in range(T_irf)])
    cw_path = np.zeros(T_irf)
    for t in range(T_irf):
        cw_path[t] = coeff * sum(params_cm.xi**k * r_shock[t + k]
                                  for k in range(1, T_irf - t))
    axes[0].plot(cw_path * 100, lw=2, label=rf'$\rho = {rho}$')

axes[0].set_xlabel('Period')
axes[0].set_ylabel(r'$c_t - w_t$ response (pp)')
axes[0].set_title(r'Response to persistent interest rate shock ($\phi = 0.8$)')
axes[0].legend(frameon=False, fontsize=8)
axes[0].grid(True, alpha=0.3)

# Panel 2: Coefficient (1 - 1/rho) vs rho
rho_range = np.linspace(0.3, 8, 200)
coeff_range = 1 - 1/rho_range
axes[1].plot(rho_range, coeff_range, lw=2, color='C0')
axes[1].axhline(0, color='gray', lw=0.8, ls='--')
axes[1].axvline(1, color='gray', lw=0.8, ls='--')
axes[1].fill_between(rho_range[rho_range < 1], coeff_range[rho_range < 1],
                      alpha=0.15, color='C1', label='Substitution dominates')
axes[1].fill_between(rho_range[rho_range > 1], coeff_range[rho_range > 1],
                      0, alpha=0.15, color='C0', label='Income dominates')
axes[1].set_xlabel(r'Risk aversion $\rho$')
axes[1].set_ylabel(r'Coefficient $1 - \rho^{-1}$')
axes[1].set_title('Income vs. substitution effects of interest rate changes')
axes[1].legend(frameon=False, fontsize=8, loc='lower right')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

## Income vs. Substitution Effects

The coefficient $(1 - \rho^{-1})$ determines how the consumption-wealth ratio responds to expected future interest rates:

| Risk aversion $\rho$ | IES $= \rho^{-1}$ | Coefficient | Interpretation |
|---|---|---|---|
| $< 1$ | $> 1$ | Negative | Substitution dominates: higher $r$ lowers $c/w$ |
| $= 1$ | $= 1$ | Zero | Income and substitution exactly cancel (log utility) |
| $> 1$ | $< 1$ | Positive | Income dominates: higher $r$ raises $c/w$ |

For the empirically relevant case $\rho > 1$, higher expected future interest rates raise the consumption-wealth ratio: the consumer feels richer and spends more today.

```{code-cell} ipython3
# Tabulate the effects for several values of rho
rows = []
for rho in [0.5, 1.0, 2.0, 3.0, 5.0]:
    ies = 1/rho
    coeff = 1 - ies
    if coeff < 0:
        interp = 'Substitution dominates'
    elif coeff == 0:
        interp = 'Effects cancel'
    else:
        interp = 'Income dominates'
    rows.append({
        'rho': rho,
        'IES': round(ies, 2),
        '1 - 1/rho': round(coeff, 2),
        'Interpretation': interp,
    })
df_effects = pd.DataFrame(rows)
df_effects
```

## The Human Wealth Channel

The Campbell-Mankiw result holds the level of total wealth $w_t$ fixed. But human wealth responds to interest rates:

$$
H_t \approx \frac{Y_t}{r - g},
$$

where $g$ is the income growth rate. A permanent decline in $r$ can increase $H_t$ enormously when $r - g$ is small. {cite:t}`summersCapTax` showed that this human wealth channel often dominates the direct income and substitution effects in general equilibrium.

```{code-cell} ipython3
# Human wealth sensitivity to interest rate changes
Y, g = 1.0, 0.02
r_grid = np.linspace(0.025, 0.10, 200)
H = Y / (r_grid - g)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(r_grid * 100, H, lw=2, color='C0')
ax.set_xlabel('Interest rate $r$ (%)')
ax.set_ylabel(r'Human wealth $H = Y/(r-g)$')
ax.set_title(f'Human wealth is highly sensitive to $r$ when $r - g$ is small ($g = {g}$)')
ax.axvline(g * 100, color='gray', ls='--', lw=0.8, label=f'$g = {g*100:.0f}\\%$')
ax.legend(frameon=False, fontsize=9)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

As $r$ approaches $g$, human wealth diverges. Even moderate interest rate changes produce large swings in $H_t$. This is why a full analysis of interest rate effects on consumption must account for the human wealth channel, not just the direct substitution and income effects on the right-hand side of the Campbell-Mankiw formula.

## Exercises

```{exercise}
:label: ex_risk_crra_mpc
Using the parameters $\beta = 1/1.04$, $\tilde{r} = 0.04$, and $\rho = 3$, compute the exact MPC $\kappa$ from [](#crra_risk_mpc) for $\sigma_r \in \{0, 0.05, 0.10, 0.15, 0.20, 0.25\}$. Compare each with the approximate formula [](#crra_risk_approx). At what level of $\sigma_r$ does the approximation error exceed 0.5 percentage points?
```

```{solution-start} ex_risk_crra_mpc
:class: dropdown
```

```{code-cell} ipython3
beta_val = 1/1.04
rho_val = 3.0
r_tilde_val = 0.04
vartheta_val = 1/beta_val - 1

rows = []
for sig in [0.0, 0.05, 0.10, 0.15, 0.20, 0.25]:
    ex = exact_mpc(rho_val, r_tilde_val, sig, beta_val)
    ap = approx_mpc(rho_val, r_tilde_val, sig, vartheta_val)
    err = abs(ex - ap)
    rows.append({
        'sigma_r': sig,
        'Exact MPC': round(ex, 6),
        'Approx MPC': round(ap, 6),
        'Error (pp)': round(err * 100, 2),
    })

df_ex1 = pd.DataFrame(rows)
df_ex1
```

The approximation error exceeds 0.5 percentage points around $\sigma_r \approx 0.20$. For moderate volatility ($\sigma_r \leq 0.15$), the linear approximation is quite accurate.

```{solution-end}
```

```{exercise}
:label: ex_risk_cara_paths
Simulate 500 consumption paths over 100 periods under the CARA model with $R = 1.04$, $\beta = 0.96$, $\alpha = 2$, $C_0 = 10$, and $\sigma_\Psi = 0.05$. Compute the average consumption growth per period across all paths and verify that it matches the theoretical prediction $\hat{\kappa} = \alpha^{-1}\log(R\beta) + \alpha\sigma_\Psi^2/2$.
```

```{solution-start} ex_risk_cara_paths
:class: dropdown
```

```{code-cell} ipython3
np.random.seed(42)
R_val, beta_val, alpha_val, sigma_val = 1.04, 0.96, 2.0, 0.05
C0, n_paths, T = 10.0, 500, 100

khat_theory = np.log(R_val * beta_val) / alpha_val + alpha_val * sigma_val**2 / 2

all_growth = []
for _ in range(n_paths):
    C = np.zeros(T)
    C[0] = C0
    for t in range(1, T):
        C[t] = C[t-1] + khat_theory + np.random.normal(0, sigma_val)
    dC = np.diff(C)
    all_growth.extend(dC.tolist())

mean_growth = np.mean(all_growth)
print(f"Theoretical expected growth:  {khat_theory:.6f}")
print(f"Simulated mean growth:       {mean_growth:.6f}")
print(f"Difference:                  {abs(khat_theory - mean_growth):.6f}")
```

The simulated mean consumption growth matches the theoretical prediction $\hat{\kappa}$ to within sampling noise, confirming [](#cara_solution).

```{solution-end}
```

```{exercise}
:label: ex_risk_cm_persistence
Consider the Campbell-Mankiw formula [](#cm_cw_ratio) with $\xi = 0.97$ and $\rho = 3$. Suppose interest rates follow an AR(1) process: $r_{t+1} = (1-\phi)\bar{r} + \phi\,r_t + \epsilon_{t+1}$, with $\bar{r} = 0.04$ and $\phi \in \{0.0, 0.5, 0.9\}$. For a 1 percentage point innovation $\epsilon_1 = 0.01$ at $t=1$, compute and plot the impulse response of $c_t - w_t$ over 40 periods for each persistence level. How does higher persistence amplify the response?
```

```{solution-start} ex_risk_cm_persistence
:class: dropdown
```

```{code-cell} ipython3
xi_val, rho_val = 0.97, 3.0
coeff = 1 - 1/rho_val
T_irf = 40
r_bar = 0.04
shock = 0.01

fig, ax = plt.subplots(figsize=(8, 4))
for phi in [0.0, 0.5, 0.9]:
    # Interest rate path after shock
    r_path = np.zeros(T_irf + 50)
    r_path[1] = shock
    for t in range(2, len(r_path)):
        r_path[t] = phi * r_path[t-1]

    # c_t - w_t at each t
    cw_response = np.zeros(T_irf)
    for t in range(T_irf):
        cw_response[t] = coeff * sum(
            xi_val**j * r_path[t + j] for j in range(1, 50)
        )

    ax.plot(cw_response * 100, lw=2, label=rf'$\phi = {phi}$')

ax.set_xlabel('Period')
ax.set_ylabel(r'$\Delta(c_t - w_t)$ (pp)')
ax.set_title(r'Higher persistence amplifies the consumption-wealth response')
ax.legend(frameon=False, fontsize=9)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

With $\phi = 0$ (no persistence), the response is a single-period blip. With $\phi = 0.9$, the shock persists, and the consumption-wealth ratio responds about $1/(1-\phi\xi) \approx 7.7$ times more on impact. Persistent interest rate shocks are far more consequential for consumption.

```{solution-end}
```

## References

```{bibliography}
:filter: docname in docnames
```
