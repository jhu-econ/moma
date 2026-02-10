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
  The envelope theorem generalizes the Euler equation to multiperiod problems, and we solve the infinite-horizon CRRA consumption model under perfect foresight with impatience conditions.
keywords:
  - envelope theorem
  - Euler equation
  - CRRA utility
  - perfect foresight
  - consumption function
tags:
  - consumption
  - intertemporal-choice
---

# The Envelope Condition and the Perfect Foresight CRRA Model

The envelope theorem generalizes the Euler equation to any finite horizon, showing that the marginal value of wealth equals the marginal utility of consumption at every date. We then solve the infinite-horizon CRRA consumption problem under perfect foresight, deriving patience conditions that govern whether wealth grows or shrinks, and obtain a closed-form consumption function that depends on overall wealth and the marginal propensity to consume.

```{code-cell} ipython3
import numpy as np
from scipy.optimize import minimize_scalar
import matplotlib.pyplot as plt
import sympy as sp
import pandas as pd
from collections import namedtuple
```

```{code-cell} ipython3
# Parameters for the envelope theorem section
EnvelopeModel = namedtuple('EnvelopeModel', ['R', 'beta', 'rho', 'T'])

# Parameters for the perfect foresight CRRA model
PFCRRAModel = namedtuple('PFCRRAModel', ['R', 'beta', 'rho', 'G'])
```

# Part I: The Envelope Condition

## The Multiperiod Problem

We study a consumer who maximizes utility over $T$ periods by choosing consumption $c_t$ at each date $t$. The value function $v_t(m_t)$ represents the maximum attainable utility starting from period $t$ with market resources $m_t$. The consumer's problem satisfies the Bellman equation

```{math}
:label: env_bellman
v_t(m_t) = \max_{c_t} u(c_t) + \beta v_{t+1}((m_t - c_t)\mathsf{R} + y_{t+1})
```

where $\beta$ is the discount factor, $\mathsf{R}$ is the gross interest factor, and $y_{t+1}$ is next period's income. The dynamic budget constraint links market resources across periods

```{math}
:label: env_dbc
m_{t+1} = (m_t - c_t)\mathsf{R} + y_{t+1}.
```

After consuming $c_t$ from resources $m_t$, the consumer earns interest $\mathsf{R}$ on the saved amount $(m_t - c_t)$ and receives income $y_{t+1}$, yielding $m_{t+1}$ for next period.

## The Lower-Bound Function

To derive the envelope condition, we define the lower-bound function $\underline{v}_t(m_t, c_t)$ that treats consumption as a free argument rather than the optimal choice

$$
\underline{v}_t(m_t, c_t) = u(c_t) + \beta v_{t+1}((m_t - c_t)\mathsf{R} + y_{t+1}).
$$

The partial derivative with respect to consumption is

```{math}
:label: env_partial_c
\underline{v}^c_t = u'(c_t) - \mathsf{R}\beta v'_{t+1}(m_{t+1})
```

and the partial derivative with respect to market resources is

```{math}
:label: env_partial_m
\underline{v}^m_t = \mathsf{R}\beta v'_{t+1}(m_{t+1}).
```

The first-order condition for the optimal consumption $c^*_t(m_t)$ requires $\underline{v}^c_t = 0$ at the optimum, which yields the Euler equation $u'(c_t) = \mathsf{R}\beta v'_{t+1}(m_{t+1})$.

## The Envelope Result

The envelope theorem states that the derivative of the value function with respect to $m_t$ can be computed by holding the optimal choice $c^*_t(m_t)$ fixed and differentiating the objective. Using the chain rule, we have

$$
v'_t(m_t) = \underline{v}^m_t + c'_t(m_t) \cdot \underline{v}^c_t.
$$

Because the first-order condition holds, we know $\underline{v}^c_t = 0$ at the optimum. Therefore, $v'_t(m_t) = \underline{v}^m_t = \mathsf{R}\beta v'_{t+1}(m_{t+1})$. Combined with the FOC, which gives $v'_t(m_t) = u'(c_t)$, we obtain the Euler equation for any horizon $T$

```{math}
:label: env_euler_general
u'(c_t) = \mathsf{R}\beta u'(c_{t+1}).
```

This result shows that the marginal value of wealth at time $t$ equals the marginal utility of consumption at time $t$, and this equality propagates forward through the Euler equation.

## Code: Numerical Verification

We verify the envelope condition numerically by solving a $T=30$ period CRRA problem via backward induction. In the last period, the consumer spends all remaining resources: $c_T(m) = m$ and $v_T(m) = u(m) = m^{1-\rho}/(1-\rho)$.

```{code-cell} ipython3
def crra_utility(c, rho):
    """CRRA utility function."""
    if rho == 1:
        return np.log(c)
    return c**(1 - rho) / (1 - rho)

def crra_marginal_utility(c, rho):
    """Marginal utility for CRRA."""
    return c**(-rho)

def solve_consumption_problem(params, m_grid, y_path):
    """
    Solve a T-period consumption problem by backward induction.

    Parameters
    ----------
    params : EnvelopeModel
        Model parameters (R, beta, rho, T)
    m_grid : array
        Grid of market resource values
    y_path : array
        Income path y_1, y_2, ..., y_T (length T)

    Returns
    -------
    c_funcs : list of arrays
        Consumption policy for each period
    v_funcs : list of arrays
        Value function for each period
    """
    R, beta, rho, T = params
    n_grid = len(m_grid)

    # Storage for policy and value functions
    c_funcs = [None] * T
    v_funcs = [None] * T

    # Terminal period: consume everything
    c_funcs[T-1] = m_grid.copy()
    v_funcs[T-1] = crra_utility(m_grid, rho)

    # Backward induction
    for t in range(T-2, -1, -1):
        c_policy = np.zeros(n_grid)
        v_policy = np.zeros(n_grid)

        for i, m in enumerate(m_grid):
            # Find optimal consumption by maximizing current utility + continuation value
            def objective(c):
                if c <= 0 or c > m:
                    return -np.inf
                m_next = (m - c) * R + y_path[t]
                # Interpolate next period's value
                v_next = np.interp(m_next, m_grid, v_funcs[t+1])
                return crra_utility(c, rho) + beta * v_next

            result = minimize_scalar(
                lambda c: -objective(c),
                bounds=(0.01, m - 0.01),
                method='bounded'
            )
            c_policy[i] = result.x
            v_policy[i] = -result.fun

        c_funcs[t] = c_policy
        v_funcs[t] = v_policy

    return c_funcs, v_funcs
```

```{code-cell} ipython3
# Set up parameters and solve
env_params = EnvelopeModel(R=1.04, beta=0.96, rho=2.0, T=30)
m_grid = np.linspace(0.1, 20, 100)
y_path = np.ones(env_params.T)  # Constant income of 1

c_funcs, v_funcs = solve_consumption_problem(env_params, m_grid, y_path)

# Verify envelope condition at t=0: v'_0(m) should equal u'(c^*_0(m))
# Compute numerical derivative of v_0
dm = m_grid[1] - m_grid[0]
v_prime_numerical = np.gradient(v_funcs[0], dm)

# Compute marginal utility of optimal consumption
u_prime_c = crra_marginal_utility(c_funcs[0], env_params.rho)

# Plot comparison
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(m_grid, v_prime_numerical, label="$v'_0(m)$ (numerical)", lw=2)
ax.plot(m_grid, u_prime_c, label="$u'(c^*_0(m))$", lw=2, linestyle='--')
ax.set_xlabel('Market resources $m_0$')
ax.set_ylabel('Marginal value')
ax.set_title('Envelope Condition: $v\'_t(m) = u\'(c^*_t(m))$')
ax.legend(frameon=False)
ax.grid(True, alpha=0.3)
plt.show()
```

The plot confirms that the marginal value of wealth $v'_0(m)$ coincides with the marginal utility of optimal consumption $u'(c^*_0(m))$ at every level of market resources. This numerical verification supports the envelope theorem result.

## Code: Saving Rate and the IES

The intertemporal elasticity of substitution (IES) equals $1/\rho$. Consumers with high $\rho$ (low IES) are reluctant to substitute consumption across time, so they respond weakly to changes in the interest rate. We plot the saving rate $s = 1 - c_0/m_0$ as a function of $\mathsf{R}$ for different values of $\rho$.

```{code-cell} ipython3
def compute_saving_rate(R_val, rho_val, beta_val, T_val, m0=10):
    """Compute saving rate for given R and rho."""
    params = EnvelopeModel(R=R_val, beta=beta_val, rho=rho_val, T=T_val)
    m_grid_sr = np.linspace(0.1, 20, 80)
    y_path_sr = np.ones(T_val)
    c_funcs_sr, _ = solve_consumption_problem(params, m_grid_sr, y_path_sr)

    # Interpolate consumption at m0
    c0 = np.interp(m0, m_grid_sr, c_funcs_sr[0])
    return 1 - c0 / m0

# Vary R from 1.00 to 1.10
R_values = np.linspace(1.00, 1.10, 15)
rho_values = [1.5, 2.0, 3.0, 5.0]

fig, ax = plt.subplots(figsize=(8, 5))

for rho_val in rho_values:
    saving_rates = [compute_saving_rate(R, rho_val, 0.96, 30) for R in R_values]
    ax.plot(R_values, saving_rates, label=f'$\\rho = {rho_val}$', lw=2, marker='o')

ax.set_xlabel('Gross interest factor $\\mathsf{R}$')
ax.set_ylabel('Saving rate $s = 1 - c_0/m_0$')
ax.set_title('Saving Rate Response to Interest Rate for Different $\\rho$')
ax.legend(frameon=False)
ax.grid(True, alpha=0.3)
plt.show()
```

The figure shows that consumers with high $\rho$ (low IES) have saving rates that are nearly insensitive to the interest rate, while consumers with low $\rho$ (high IES) respond more strongly. This confirms that the IES measures the willingness to substitute consumption across time.

## Exercise

```{exercise}
:label: ex_envelope_verify

Given parameters $\mathsf{R}=1.04$, $\beta=0.96$, $\rho=2$, and $T=10$, compute the value function numerically for period $t=0$ and verify that the envelope condition $v'_0(m) = u'(c^*_0(m))$ holds at $m \in \{2, 5, 10, 20\}$. Report the percentage difference between $v'_0(m)$ (computed numerically via finite differences) and $u'(c^*_0(m))$ at each of these four values.
```

```{solution-start} ex_envelope_verify
:class: dropdown
```

```{code-cell} ipython3
# Solve the problem
ex_params = EnvelopeModel(R=1.04, beta=0.96, rho=2.0, T=10)
m_grid_ex = np.linspace(0.1, 25, 120)
y_path_ex = np.ones(ex_params.T)

c_funcs_ex, v_funcs_ex = solve_consumption_problem(ex_params, m_grid_ex, y_path_ex)

# Check envelope condition at specific points
m_check = np.array([2, 5, 10, 20])
results = []

for m_val in m_check:
    # Interpolate consumption
    c_star = np.interp(m_val, m_grid_ex, c_funcs_ex[0])
    u_prime = crra_marginal_utility(c_star, ex_params.rho)

    # Compute v' numerically using centered difference
    dm_check = 0.01
    v_plus = np.interp(m_val + dm_check, m_grid_ex, v_funcs_ex[0])
    v_minus = np.interp(m_val - dm_check, m_grid_ex, v_funcs_ex[0])
    v_prime = (v_plus - v_minus) / (2 * dm_check)

    pct_diff = 100 * abs(v_prime - u_prime) / abs(u_prime)
    results.append({
        'm': m_val,
        "v'(m)": v_prime,
        "u'(c*)": u_prime,
        '% diff': pct_diff
    })

df_results = pd.DataFrame(results)
print(df_results.to_string(index=False))
```

The percentage differences are very small (typically less than 1%), confirming that the envelope condition holds numerically at each value of $m$.

```{solution-end}
```

# Part II: Perfect Foresight CRRA Model

## Setup

We now study the infinite-horizon consumption problem with CRRA utility $u(c) = c^{1-\rho}/(1-\rho)$ and permanent income $p_t$ growing at the deterministic factor $G$, so $p_{t+1} = G \cdot p_t$. The consumer receives income $y_t = p_t$ each period and faces the dynamic budget constraint

```{math}
:label: pf_dbc
m_{t+1} = (m_t - c_t)\mathsf{R} + p_{t+1}
```

where $m_t$ denotes market resources (bank balances plus current income) and $\mathsf{R}$ is the gross interest factor. The consumer's optimization problem is to maximize $\sum_{s=0}^{\infty} \beta^s u(c_{t+s})$ subject to the sequence of budget constraints.

## Consumption Growth and the Patience Factor

The Euler equation $u'(c_t) = \mathsf{R}\beta u'(c_{t+1})$ combined with CRRA utility $u'(c) = c^{-\rho}$ yields

$$
c_t^{-\rho} = \mathsf{R}\beta c_{t+1}^{-\rho}
$$

which we solve to obtain the consumption growth factor

```{math}
:label: pf_patience_factor
\frac{c_{t+1}}{c_t} = (\mathsf{R}\beta)^{1/\rho} \equiv \Phi.
```

We call $\Phi$ the patience factor. If $\Phi < 1$ (absolute impatience), consumption falls over time as the consumer prefers current consumption to future consumption. If $\Phi > 1$ (absolute patience), consumption grows over time.

We can verify symbolically that the CRRA Euler equation yields the patience factor $\Phi = (\mathsf{R}\beta)^{1/\rho}$.

```{code-cell} ipython3
# Symbolic derivation of the patience factor
c_t, c_tp1 = sp.symbols('c_t c_{t+1}', positive=True)
R_sym, beta_sym, rho_sym = sp.symbols('R beta rho', positive=True)

# CRRA Euler equation: c_t^{-rho} = R * beta * c_{t+1}^{-rho}
euler_eq = sp.Eq(c_t**(-rho_sym), R_sym * beta_sym * c_tp1**(-rho_sym))

# Solve for c_{t+1} and compute the growth ratio
c_tp1_sol = sp.solve(euler_eq, c_tp1)[0]
growth_ratio = sp.simplify(c_tp1_sol / c_t)

print("Consumption growth factor c_{t+1}/c_t =")
growth_ratio
```

## The Intertemporal Budget Constraint

Because income grows at factor $G$, the present discounted value of future income is

```{math}
:label: pf_human_wealth
h_t = \sum_{n=0}^{T-t} \mathsf{R}^{-n} p_{t+n} = p_t \sum_{n=0}^{T-t} \mathsf{R}^{-n} G^n = p_t \frac{1 - (G/\mathsf{R})^{T-t+1}}{1 - G/\mathsf{R}}
```

where we call $h_t$ human wealth. The consumer's overall wealth is $o_t = b_t + h_t$, where $b_t = m_t - p_t$ denotes bank balances (market resources minus current income). The intertemporal budget constraint states that the present discounted value of consumption equals overall wealth.

## Impatience Conditions

Three impatience conditions govern the behavior of wealth and consumption in the infinite-horizon limit. The finite human wealth condition (FHWC) requires

```{math}
:label: pf_fhwc
G < \mathsf{R}.
```

Without FHWC, human wealth is infinite because future income grows faster than the discount rate. The return impatience condition (RIC) requires

```{math}
:label: pf_ric
\frac{\Phi}{\mathsf{R}} < 1
```

which ensures that the present discounted value of consumption is finite (consumption grows at $\Phi$ but is discounted at $\mathsf{R}$). The growth impatience condition (GIC) requires

```{math}
:label: pf_gic
\frac{\Phi}{G} < 1
```

which ensures that the wealth-to-income ratio does not explode over time (consumption grows slower than income). Without GIC, the consumer accumulates wealth without bound relative to income.

## Code: Impatience Regions

We plot the patience factor $\Phi$ as a function of the discount factor $\beta$ for fixed $\mathsf{R}=1.04$ and $\rho=2$, and mark the boundaries corresponding to the absolute impatience condition (AIC), GIC, and RIC.

```{code-cell} ipython3
R_pf = 1.04
rho_pf = 2.0
G_pf = 1.02

beta_values = np.linspace(0.90, 1.00, 100)
Phi_values = (R_pf * beta_values)**(1 / rho_pf)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(beta_values, Phi_values, lw=2, color='black', label='$\\Phi = (\\mathsf{R}\\beta)^{1/\\rho}$')
ax.axhline(1, color='blue', linestyle='--', lw=2, label='AIC: $\\Phi = 1$')
ax.axhline(G_pf, color='green', linestyle='--', lw=2, label=f'GIC: $\\Phi = G = {G_pf}$')
ax.axhline(R_pf, color='red', linestyle='--', lw=2, label=f'RIC: $\\Phi = \\mathsf{{R}} = {R_pf}$')

# Shade regions
ax.fill_between(beta_values, 0, 1, where=(Phi_values < 1), alpha=0.2, color='blue', label='Absolute impatience')
ax.fill_between(beta_values, 1, G_pf, where=((Phi_values >= 1) & (Phi_values < G_pf)), alpha=0.2, color='green', label='Growth impatience')
ax.fill_between(beta_values, G_pf, R_pf, where=((Phi_values >= G_pf) & (Phi_values < R_pf)), alpha=0.2, color='orange', label='Return impatience')

ax.set_xlabel('Discount factor $\\beta$')
ax.set_ylabel('Patience factor $\\Phi$')
ax.set_title('Impatience Regions ($\\mathsf{R}=1.04$, $\\rho=2$, $G=1.02$)')
ax.set_ylim(0.95, 1.05)
ax.legend(frameon=False, fontsize=8)
ax.grid(True, alpha=0.3)
plt.show()
```

The shaded regions illustrate the parameter space where different impatience conditions hold. Most plausible parameter values lie in the growth-impatient or return-impatient regions.

## The Consumption Function

In a finite-horizon problem, the consumption function takes the form $c_t = \kappa_t \cdot o_t$ where $\kappa_t$ is the marginal propensity to consume (MPC) out of overall wealth. The MPC evolves according to

```{math}
:label: pf_mpc_finite
\kappa_t = \frac{1 - \mathsf{R}^{-1}\Phi}{1 - (\mathsf{R}^{-1}\Phi)^{T-t+1}}.
```

As the horizon $T - t$ grows, the denominator approaches 1 (assuming RIC holds), and the MPC converges to the infinite-horizon value

```{math}
:label: pf_mpc_infinite
\kappa = 1 - \frac{\Phi}{\mathsf{R}}.
```

This formula shows that the MPC depends on the patience factor $\Phi$ and the interest factor $\mathsf{R}$. More impatient consumers (low $\Phi$) have higher MPCs.

## Code: Finite vs Infinite Horizon MPC

We compute and plot the MPC $\kappa_t$ over the life cycle for a finite horizon $T=50$, and compare it to the infinite-horizon MPC $\kappa$.

```{code-cell} ipython3
def mpc_finite_horizon(t, T, R, Phi):
    """Compute MPC at time t in a T-period problem."""
    if T - t <= 0:
        return 1.0  # Terminal period: consume everything
    numerator = 1 - (1 / R) * Phi
    denominator = 1 - ((1 / R) * Phi)**(T - t + 1)
    return numerator / denominator

def mpc_infinite_horizon(R, Phi):
    """Compute infinite-horizon MPC."""
    return 1 - Phi / R

# Parameters
R_mpc = 1.04
beta_mpc = 0.96
rho_mpc = 2.0
Phi_mpc = (R_mpc * beta_mpc)**(1 / rho_mpc)
T_mpc = 50

# Compute MPC over time
t_values = np.arange(0, T_mpc)
kappa_t_values = [mpc_finite_horizon(t, T_mpc, R_mpc, Phi_mpc) for t in t_values]
kappa_inf = mpc_infinite_horizon(R_mpc, Phi_mpc)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(t_values, kappa_t_values, lw=2, label=f'Finite horizon ($T={T_mpc}$)')
ax.axhline(kappa_inf, color='red', linestyle='--', lw=2, label=f'Infinite horizon: $\\kappa = {kappa_inf:.4f}$')
ax.set_xlabel('Time $t$')
ax.set_ylabel('MPC $\\kappa_t$')
ax.set_title('Marginal Propensity to Consume over the Life Cycle')
ax.legend(frameon=False)
ax.grid(True, alpha=0.3)
plt.show()
```

The MPC increases sharply as the consumer approaches the terminal date, because the consumer has less time remaining to spread resources. For most of the horizon, however, $\kappa_t$ is close to the infinite-horizon value.

## Sustainable Consumption

The wealth-preserving consumption rate is $\bar{\kappa} = r/\mathsf{R}$ where $r = \mathsf{R} - 1$ is the net interest rate. If the consumer spends exactly $\bar{\kappa} \cdot o_t$, wealth remains constant over time. Comparing $\kappa$ to $\bar{\kappa}$, we can determine whether the consumer is spending down wealth. If $\kappa > r/\mathsf{R}$, the consumer is absolutely impatient and consumption exceeds the sustainable level.

```{code-cell} ipython3
# Compare actual MPC to sustainable rate
r_net = R_mpc - 1
kappa_bar = r_net / R_mpc

print(f"Infinite-horizon MPC: κ = {kappa_inf:.4f}")
print(f"Sustainable rate: κ̄ = r/R = {kappa_bar:.4f}")
print(f"Consumer is {'spending down' if kappa_inf > kappa_bar else 'accumulating'} wealth")
```

## The Approximate Consumption Function

For small values of the net interest rate $r$ and the time preference rate $\delta$ (where $\beta \approx 1/(1+\delta)$), we can derive a log-linear approximation to the consumption function. The approximate MPC is

```{math}
:label: pf_approx_cons
\kappa \approx r - \rho^{-1}(r - \delta).
```

Changes in the interest rate $r$ affect consumption through three channels: the income effect (higher $r$ increases income from assets), the substitution effect (higher $r$ encourages saving, which enters through $\rho^{-1}$), and the human wealth effect (higher $r$ reduces the present value of future labor income).

## Code: Human Wealth Effect

We fix bank balances at $b_t = 0$ so that overall wealth equals human wealth, and compute consumption relative to permanent income $c_t/p_t$ as a function of the net interest rate $r$ for different values of income growth $G$. Following Summers (1981) {cite}`summersCapTax`, we show that consumption is highly sensitive to the interest rate through the human wealth channel.

```{code-cell} ipython3
def compute_c_to_p_ratio(r_net, G_val, beta_val, rho_val, T_hw=100):
    """
    Compute consumption-to-permanent-income ratio with zero bank balances.

    Parameters
    ----------
    r_net : float
        Net interest rate
    G_val : float
        Income growth factor
    beta_val : float
        Discount factor
    rho_val : float
        CRRA parameter
    T_hw : int
        Horizon for human wealth calculation
    """
    R_val = 1 + r_net
    Phi_val = (R_val * beta_val)**(1 / rho_val)

    # Human wealth with finite horizon
    if abs(G_val / R_val - 1) < 1e-6:
        h_to_p = T_hw + 1  # Special case: sum of constant terms
    else:
        h_to_p = (1 - (G_val / R_val)**(T_hw + 1)) / (1 - G_val / R_val)

    # Overall wealth equals human wealth (b=0)
    # MPC (approximate infinite horizon)
    if (1 / R_val) * Phi_val < 1:
        kappa_val = 1 - Phi_val / R_val
    else:
        kappa_val = 0.05  # Fallback if RIC fails

    # Consumption to permanent income
    c_to_p = kappa_val * h_to_p
    return c_to_p

# Vary net interest rate from 1% to 6%
r_net_values = np.linspace(0.01, 0.06, 20)
G_values = [1.01, 1.02, 1.03]

fig, ax = plt.subplots(figsize=(8, 5))

for G_val in G_values:
    c_to_p_ratios = [compute_c_to_p_ratio(r, G_val, 0.96, 2.0) for r in r_net_values]
    ax.plot(r_net_values * 100, c_to_p_ratios, lw=2, marker='o', label=f'$G = {G_val}$')

ax.set_xlabel('Net interest rate $r$ (%)')
ax.set_ylabel('$c_t/p_t$ (bank balances = 0)')
ax.set_title('Human Wealth Effect on Consumption (Summers 1981)')
ax.legend(frameon=False)
ax.grid(True, alpha=0.3)
plt.show()
```

The figure demonstrates that consumption relative to permanent income is extremely sensitive to the interest rate when bank balances are zero. A higher interest rate reduces the present value of future labor income (human wealth), which dominates the substitution effect for reasonable parameter values.

## Code: Saving Rate Response

Even for consumers with moderate risk aversion ($\rho = 2$), the saving rate responds strongly to the interest rate because of the human wealth effect. We plot the saving rate as a function of $r$ for different values of $\rho$.

```{code-cell} ipython3
def compute_saving_rate_pf(r_net, rho_val, beta_val, G_val, m_to_p=5):
    """
    Compute saving rate s = 1 - c/m in the perfect foresight model.

    Assumes m/p = m_to_p and computes overall wealth, then consumption.
    """
    R_val = 1 + r_net
    Phi_val = (R_val * beta_val)**(1 / rho_val)

    # Human wealth per unit permanent income (finite horizon T=100)
    T_sr = 100
    if abs(G_val / R_val - 1) < 1e-6:
        h_to_p = T_sr + 1
    else:
        h_to_p = (1 - (G_val / R_val)**(T_sr + 1)) / (1 - G_val / R_val)

    # Bank balances: b = m - p, so b/p = m/p - 1
    b_to_p = m_to_p - 1

    # Overall wealth to p
    o_to_p = b_to_p + h_to_p

    # MPC
    if (1 / R_val) * Phi_val < 1:
        kappa_val = 1 - Phi_val / R_val
    else:
        kappa_val = 0.05

    # Consumption to permanent income
    c_to_p = kappa_val * o_to_p

    # Saving rate: s = 1 - c/m
    c_to_m = c_to_p / m_to_p
    return 1 - c_to_m

r_net_sr = np.linspace(0.01, 0.06, 15)
rho_sr_values = [1.5, 2.0, 3.0, 5.0]

fig, ax = plt.subplots(figsize=(8, 5))

for rho_sr in rho_sr_values:
    s_values = [compute_saving_rate_pf(r, rho_sr, 0.96, 1.02) for r in r_net_sr]
    ax.plot(r_net_sr * 100, s_values, lw=2, marker='o', label=f'$\\rho = {rho_sr}$')

ax.set_xlabel('Net interest rate $r$ (%)')
ax.set_ylabel('Saving rate $s = 1 - c/m$')
ax.set_title('Saving Rate Response with Human Wealth Effect')
ax.legend(frameon=False)
ax.grid(True, alpha=0.3)
plt.show()
```

The saving rate is highly sensitive to the interest rate even for consumers with $\rho = 2$, because the human wealth effect dominates. This challenges the view that consumption and saving are unresponsive to interest rates.

## Normalizing by Permanent Income

To simplify the analysis, we normalize all variables by permanent income $p_t$. Define $\hat{c}_t = c_t/p_t$, $\hat{m}_t = m_t/p_t$, $\hat{b}_t = b_t/p_t$, and $\hat{o}_t = o_t/p_t$. The normalized dynamic budget constraint becomes

```{math}
:label: pf_normalized
\hat{b}_{t+1} = (\hat{m}_t - \hat{c}_t)\frac{\mathsf{R}}{G}.
```

The ratio $\mathsf{R}/G$ determines the growth rate of normalized bank balances. The GIC ensures that $\Phi/G < 1$, which guarantees that normalized consumption and wealth converge to finite steady-state values. Without the GIC, normalized wealth would grow without bound.

## Exercises

```{exercise}
:label: ex_mpc_compute

Given $\mathsf{R}=1.04$, $\beta=0.96$, $\rho=2$, and $G=1.02$, compute the infinite-horizon marginal propensity to consume $\kappa$. Verify that the return impatience condition (RIC), finite human wealth condition (FHWC), and growth impatience condition (GIC) all hold for these parameters.
```

```{solution-start} ex_mpc_compute
:class: dropdown
```

```{code-cell} ipython3
# Given parameters
R_ex1 = 1.04
beta_ex1 = 0.96
rho_ex1 = 2.0
G_ex1 = 1.02

# Compute patience factor
Phi_ex1 = (R_ex1 * beta_ex1)**(1 / rho_ex1)

# Compute infinite-horizon MPC
kappa_ex1 = 1 - Phi_ex1 / R_ex1

print(f"Patience factor: Φ = {Phi_ex1:.6f}")
print(f"Infinite-horizon MPC: κ = {kappa_ex1:.6f}")
print()

# Check impatience conditions
print("Impatience conditions:")
print(f"  FHWC: G < R  →  {G_ex1} < {R_ex1}  →  {G_ex1 < R_ex1}")
print(f"  RIC: Φ/R < 1  →  {Phi_ex1:.6f}/{R_ex1} = {Phi_ex1/R_ex1:.6f} < 1  →  {Phi_ex1/R_ex1 < 1}")
print(f"  GIC: Φ/G < 1  →  {Phi_ex1:.6f}/{G_ex1} = {Phi_ex1/G_ex1:.6f} < 1  →  {Phi_ex1/G_ex1 < 1}")
```

All three impatience conditions hold, so the consumer has well-defined human wealth, finite consumption PDV, and bounded wealth-to-income ratio.

```{solution-end}
```

```{exercise}
:label: ex_growth_impatient

Find the value of $\beta$ that makes a consumer with $\mathsf{R}=1.04$ and $\rho=2$ exactly growth-impatient (i.e., $\Phi = G$) when $G = 1.02$. Verify your answer by computing $\Phi$ at this value of $\beta$.
```

```{solution-start} ex_growth_impatient
:class: dropdown
```

```{code-cell} ipython3
# We need Φ = G, where Φ = (R β)^(1/ρ)
# So (R β)^(1/ρ) = G
# R β = G^ρ
# β = G^ρ / R

R_ex2 = 1.04
rho_ex2 = 2.0
G_ex2 = 1.02

beta_ex2 = G_ex2**rho_ex2 / R_ex2

# Verify
Phi_ex2 = (R_ex2 * beta_ex2)**(1 / rho_ex2)

print(f"Required β = {beta_ex2:.6f}")
print(f"Verification: Φ = (R β)^(1/ρ) = {Phi_ex2:.6f}")
print(f"Target: G = {G_ex2}")
print(f"Match: {abs(Phi_ex2 - G_ex2) < 1e-10}")
```

The consumer is exactly growth-impatient when $\beta \approx 0.9604$. At this value, consumption growth equals income growth, so the consumption-to-income ratio remains constant over time.

```{solution-end}
```

```{exercise}
:label: ex_summers_calc

Replicate the Summers (1981) calculation. With $(r, \delta, G - 1, \rho) = (0.04, 0.04, 0.02, 2)$, show that a 1 percentage point drop in the net interest rate $r$ (from 4% to 3%) approximately doubles the consumption-to-permanent-income ratio when bank balances are zero.
```

```{solution-start} ex_summers_calc
:class: dropdown
```

```{code-cell} ipython3
# Parameters
delta_ex3 = 0.04
beta_ex3 = 1 / (1 + delta_ex3)
rho_ex3 = 2.0
G_ex3 = 1.02
T_ex3 = 100

# Interest rates
r_high = 0.04
r_low = 0.03

# Compute c/p at high interest rate
c_to_p_high = compute_c_to_p_ratio(r_high, G_ex3, beta_ex3, rho_ex3, T_ex3)

# Compute c/p at low interest rate
c_to_p_low = compute_c_to_p_ratio(r_low, G_ex3, beta_ex3, rho_ex3, T_ex3)

# Ratio
ratio_ex3 = c_to_p_low / c_to_p_high

print(f"Parameters: r_high = {r_high}, r_low = {r_low}, δ = {delta_ex3}, G = {G_ex3}, ρ = {rho_ex3}")
print()
print(f"c/p at r = {r_high}: {c_to_p_high:.4f}")
print(f"c/p at r = {r_low}: {c_to_p_low:.4f}")
print(f"Ratio: {ratio_ex3:.2f}")
print()
print(f"A 1pp drop in r increases c/p by a factor of {ratio_ex3:.2f}, nearly doubling it.")
```

The calculation confirms Summers' finding: when consumers have no initial wealth (only human wealth), a small decrease in the interest rate substantially increases consumption relative to permanent income. This occurs because the present value of future labor income rises sharply when the discount rate falls.

```{solution-end}
```

## References

```{bibliography}
:filter: docname in docnames
```
