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
  The consumption random walk and the permanent income hypothesis:
  Hall's unpredictability result and the consumption function with
  permanent versus transitory shocks
keywords:
  - random walk
  - permanent income hypothesis
  - Hall
  - Muth
  - MPC
tags:
  - consumption
  - intertemporal-choice
---

# The Consumption Random Walk and the Permanent Income Hypothesis

Part I derives Hall's random walk proposition from quadratic utility and $\mathsf{R}\beta = 1$: consumption changes are unpredictable. Part II derives the consumption function with permanent versus transitory income shocks, showing that the MPC depends on whether a shock is permanent or transitory (Muth's insight).

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import sympy as sp
from collections import namedtuple
import pandas as pd
```

```{code-cell} ipython3
# Parameters for random walk model
RandomWalkModel = namedtuple(
    'RandomWalkModel',
    ['R', 'beta', 'c_bar', 'T']
)

# Parameters for permanent income model
PermIncomeModel = namedtuple(
    'PermIncomeModel',
    ['R', 'beta', 'sigma_psi', 'sigma_theta', 'T']
)
```

## Part I: The Consumption Random Walk

### From Euler Equation to Random Walk

We start with the Euler equation under uncertainty, which requires that the marginal utility of consumption today equals the expected discounted marginal utility of consumption tomorrow:

```{math}
:label: rw_euler_uncertain
u'(c_t) = \mathsf{R}\beta \, \mathbb{E}_t[u'(c_{t+1})].
```

Consider quadratic utility $u(c) = -(1/2)(\bar{c} - c)^2$, where the bliss point $\bar{c}$ represents the satiation level of consumption. The marginal utility is $u'(c) = \bar{c} - c$, which is linear in consumption $c$. When we impose the condition $\mathsf{R}\beta = 1$, the discount factor exactly offsets the interest rate, and the Euler equation becomes

$$
\bar{c} - c_t = \mathbb{E}_t[\bar{c} - c_{t+1}],
$$

which simplifies to $\mathbb{E}_t[c_{t+1}] = c_t$. Consumption follows a martingale: today's consumption is the best forecast of tomorrow's consumption.

### Hall's Proposition

Define the consumption innovation as the first difference $\epsilon_{t+1} = c_{t+1} - c_t \equiv \Delta c_{t+1}$. Taking expectations at time $t$, we obtain Hall's random walk result:

```{math}
:label: rw_hall_result
\mathbb{E}_t[\Delta c_{t+1}] = 0.
```

This result states that consumption changes are unpredictable. No lagged variable known at time $t$ (past income, past consumption, past interest rates) can predict $\Delta c_{t+1}$. Hall {cite}`hallRandomWalk` showed that this proposition provides a way to test the life cycle-permanent income hypothesis without specifying the income process, a major breakthrough in empirical macroeconomics.

:::{note}
Hall's random walk proposition was revolutionary because it gave researchers a way to test the theory without needing to model the income process explicitly. Earlier tests required detailed assumptions about income dynamics, which were difficult to verify.
:::

### Code: Simulating a Random Walk

We simulate a single consumer whose consumption follows a random walk. With the gross interest factor $\mathsf{R} = 1.04$ and discount factor $\beta = 1/\mathsf{R}$, the condition $\mathsf{R}\beta = 1$ holds exactly.

```{code-cell} ipython3
# Set parameters
np.random.seed(42)
params = RandomWalkModel(R=1.04, beta=1/1.04, c_bar=100, T=100)
sigma_eps = 2.0

# Simulate consumption path
c = np.zeros(params.T)
c[0] = 50.0
eps = np.random.normal(0, sigma_eps, params.T - 1)

for t in range(1, params.T):
    c[t] = c[t-1] + eps[t-1]

# Compute consumption changes
delta_c = np.diff(c)
c_lagged = c[:-1]

# Create plots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

# Left panel: consumption level over time
ax1.plot(c, lw=2, color='darkblue')
ax1.set_xlabel('Time')
ax1.set_ylabel('Consumption')
ax1.set_title('Random Walk Consumption Path')
ax1.grid(True, alpha=0.3)

# Right panel: scatter plot of changes vs lagged level
ax2.scatter(c_lagged, delta_c, alpha=0.5, s=20, color='darkblue')
ax2.axhline(0, color='red', linestyle='--', lw=1.5, label='Zero mean')
ax2.set_xlabel('$c_t$')
ax2.set_ylabel('$\\Delta c_{t+1}$')
ax2.set_title('Consumption Changes vs Lagged Level')
ax2.legend(frameon=False)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

The left panel shows the consumption level wandering randomly. The right panel confirms that consumption changes $\Delta c_{t+1}$ have zero correlation with the lagged consumption level $c_t$: knowing where consumption is today tells us nothing about which direction it will move tomorrow.

### Code: Cross-Sectional Implications

We simulate 250 independent consumers, each following a random walk for $T = 60$ periods. The variance of consumption across consumers grows linearly with time because each period adds an independent shock with variance $\sigma^2$.

```{code-cell} ipython3
# Cross-sectional simulation
np.random.seed(2024)
N = 250
T = 60
sigma_eps = 2.0

# Initial consumption drawn from a distribution
c0_mean = 50.0
c0_std = 5.0
c_initial = np.random.normal(c0_mean, c0_std, N)

# Store consumption for all consumers
consumption = np.zeros((N, T))
consumption[:, 0] = c_initial

# Simulate each consumer
for i in range(N):
    eps = np.random.normal(0, sigma_eps, T - 1)
    for t in range(1, T):
        consumption[i, t] = consumption[i, t-1] + eps[t-1]

# Compute variance across consumers at each time
var_c = np.var(consumption, axis=0)

# Theoretical prediction: Var(c_t) = Var(c_0) + t * sigma^2
theoretical_var = c0_std**2 + np.arange(T) * sigma_eps**2

# Plot
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(var_c, lw=2, label='Simulated variance', color='darkblue')
ax.plot(theoretical_var, lw=2, linestyle='--', label='Theoretical: $\\mathrm{Var}(c_0) + t\\sigma^2$', color='red')
ax.set_xlabel('Time')
ax.set_ylabel('Variance of consumption')
ax.set_title('Cross-Sectional Consumption Variance')
ax.legend(frameon=False)
ax.grid(True, alpha=0.3)
plt.show()
```

The simulated variance matches the theoretical prediction $\text{Var}(c_t) = \text{Var}(c_0) + t \cdot \sigma^2$ closely. Deaton and Paxson {cite}`deatonPaxson1994` documented that cross-sectional consumption inequality grows with age in household data, consistent with the random walk model when consumers face idiosyncratic income shocks.

### Strengths and Limitations

The consumption random walk has three key strengths. First, it is testable without specifying the income process, which was Hall's major contribution. Second, it provides clear cross-sectional predictions about inequality. Third, it delivers a simple null hypothesis for regression tests.

However, the model has important limitations. Limitation one: the result requires quadratic utility, which implies linear marginal utility. With CRRA utility $u(c) = c^{1-\rho}/(1-\rho)$, marginal utility is convex, and consumption changes would be predictable by anything correlated with $\text{Var}_{t}(c_{t+1})$. Limitation two: the result requires $\mathsf{R}\beta = 1$ exactly. If $\mathsf{R}\beta \neq 1$, consumption has a deterministic drift. Limitation three: quadratic utility ignores precautionary saving because the third derivative of utility is zero, ruling out prudence.

### Exercise: Testing Predictability

```{exercise}
:label: ex_rw_regression

Simulate 500 periods of a random walk consumer with initial consumption $c_0 = 50$, shock standard deviation $\sigma = 2$, and $\mathsf{R}\beta = 1$. Run two regressions: (a) regress $\Delta c_{t+1}$ on $c_t$, and (b) regress $\Delta c_{t+1}$ on $c_{t-1}$. Report the estimated coefficients and $R^2$ values. Verify that neither lagged variable has predictive power.
```

```{solution-start} ex_rw_regression
:class: dropdown
```

```{code-cell} ipython3
# Simulate 500 periods
np.random.seed(100)
T = 500
c = np.zeros(T)
c[0] = 50.0
eps = np.random.normal(0, 2.0, T - 1)

for t in range(1, T):
    c[t] = c[t-1] + eps[t-1]

# Prepare regression data
delta_c = np.diff(c)  # Length T-1
c_lag0 = c[:-1]       # c_t, length T-1
c_lag1 = c[:-2]       # c_{t-1}, length T-2
delta_c_for_lag1 = delta_c[1:]  # Length T-2

# Regression (a): Delta c_{t+1} on c_t
reg_a = stats.linregress(c_lag0, delta_c)

# Regression (b): Delta c_{t+1} on c_{t-1}
reg_b = stats.linregress(c_lag1, delta_c_for_lag1)

# Display results
results = pd.DataFrame({
    'Regression': ['(a) on $c_t$', '(b) on $c_{t-1}$'],
    'Intercept': [reg_a.intercept, reg_b.intercept],
    'Slope': [reg_a.slope, reg_b.slope],
    'R²': [reg_a.rvalue**2, reg_b.rvalue**2]
})

print(results.to_string(index=False))
```

The coefficients on lagged consumption are negligible (near zero), and the $R^2$ values are close to zero. Neither $c_t$ nor $c_{t-1}$ predicts consumption changes, confirming Hall's random walk proposition.

```{solution-end}
```

## Part II: The Consumption Function

### The CEQ Consumer

We now derive the consumption function for a consumer with quadratic utility and $\mathsf{R}\beta = 1$. The consumer chooses consumption $c_t$ subject to the budget constraint

```{math}
:label: cf_budget
b_{t+1} = (b_t + y_t - c_t)\mathsf{R},
```

where the bank balance $b_t$ represents financial wealth at the beginning of period $t$, and income $y_t$ is received during period $t$.

### The Income Process

Income has two components. The permanent component $p_t$ evolves according to a random walk:

$$
p_{t+1} = p_t + \psi_{t+1},
$$

where the permanent shock $\psi_{t+1}$ is white noise with $\mathbb{E}_t[\psi_{t+n}] = 0$ for all $n > 0$. Observed income includes a transitory component:

```{math}
:label: cf_income_process
y_{t+1} = p_{t+1} + \theta_{t+1},
```

where the transitory shock $\theta_{t+1}$ is also white noise with $\mathbb{E}_t[\theta_{t+n}] = 0$ for $n > 0$. Permanent shocks affect all future income, while transitory shocks affect only current income.

### Solving via the IBC

The intertemporal budget constraint equates the expected present discounted value of consumption to the expected present discounted value of total resources. Because consumption follows a random walk, we have $\mathbb{E}_t[c_{t+n}] = c_t$ for all $n \geq 0$. The present value of consumption is therefore

$$
\sum_{n=0}^{\infty} \mathsf{R}^{-n} c_t = c_t \sum_{n=0}^{\infty} \mathsf{R}^{-n} = c_t \cdot \frac{1}{1 - \mathsf{R}^{-1}} = c_t \cdot \frac{\mathsf{R}}{\mathsf{R} - 1}.
$$

Defining the interest rate $r = \mathsf{R} - 1$, the present value of consumption simplifies to $c_t \cdot \mathsf{R}/r$.

The present value of total resources includes current bank balances $b_t$, the transitory shock $\theta_t$ (which contributes only in the current period), and the present value of permanent income. Since $\mathbb{E}_t[y_{t+n}] = p_t$ for all $n > 0$, the present value of future income is

$$
\sum_{n=1}^{\infty} \mathsf{R}^{-n} p_t = p_t \sum_{n=1}^{\infty} \mathsf{R}^{-n} = p_t \cdot \frac{\mathsf{R}^{-1}}{1 - \mathsf{R}^{-1}} = p_t \cdot \frac{1}{\mathsf{R} - 1} = \frac{p_t}{r}.
$$

Including current income $y_t = p_t + \theta_t$, the total present value of resources is $b_t + p_t + \theta_t + p_t/r$. Equating consumption and resources gives

```{math}
:label: cf_consumption_fn
c_t = \frac{r}{\mathsf{R}}(b_t + \theta_t) + p_t.
```

We can derive this result symbolically by equating the present discounted values and solving for consumption.

```{code-cell} ipython3
# Symbolic derivation of the consumption function from the IBC
c_sym, b_sym, p_sym, theta_sym = sp.symbols('c_t b_t p_t theta_t', positive=True)
R_sym, r_sym = sp.symbols('R r', positive=True)

# PDV of consumption (random walk => E[c_{t+n}] = c_t for all n)
pdv_consumption = c_sym * R_sym / r_sym

# PDV of total resources: bank balances + current income + future income
pdv_resources = b_sym + (p_sym + theta_sym) + p_sym / r_sym

# Equate and solve for c_t
ibc = sp.Eq(pdv_consumption, pdv_resources)
c_sol = sp.solve(ibc, c_sym)[0]

# Substitute R = 1 + r and simplify
c_simplified = sp.simplify(c_sol.subs(R_sym, 1 + r_sym))
print("Consumption function:")
c_simplified
```

This consumption function reveals that the consumer treats bank balances and transitory income identically (both are multiplied by $r/\mathsf{R}$), consuming only the annuity value. In contrast, permanent income $p_t$ is consumed one-for-one because it represents an annuity that already lasts forever.

### Muth's Insight: MPC by Shock Type

The consumption function {eq}`cf_consumption_fn` implies two distinct marginal propensities to consume. The transitory MPC is

$$
\frac{\partial c}{\partial \theta} = \frac{r}{\mathsf{R}} \approx 0.05
$$

when the interest rate $r = 0.04$. Only the annuity value of the transitory shock is consumed. The permanent MPC is

$$
\frac{\partial c}{\partial p} = 1,
$$

because the full shock is consumed immediately. A permanent shock is equivalent to receiving an annuity that pays $\Delta p$ in every period forever, so the consumer can afford to raise consumption by exactly $\Delta p$.

```{code-cell} ipython3
# Compute MPC by shock type for different interest rates
r_values = np.array([0.02, 0.04, 0.06, 0.10])
R_values = 1 + r_values
mpc_transitory = r_values / R_values
mpc_permanent = np.ones_like(r_values)

mpc_table = pd.DataFrame({
    'Interest rate $r$': r_values,
    'Transitory MPC': mpc_transitory,
    'Permanent MPC': mpc_permanent
})

print("\nMarginal Propensities to Consume by Shock Type")
print("=" * 60)
print(mpc_table.to_string(index=False))
```

This distinction explains why the "Keynesian consumption function" $c_t = \alpha_0 + \alpha_1 y_t$ is problematic. There is no single "true" $\alpha_1$: the estimated coefficient depends on the mix of permanent and transitory shocks in the data. Muth {cite}`muthOptimal` recognized that distinguishing shock types is essential for understanding consumption behavior.

### Code: Transitory vs Permanent Shocks Simulation

We simulate a consumer for $T = 80$ periods with both permanent and transitory income shocks. The permanent shock has standard deviation $\sigma_\psi = 0.5$, while the transitory shock has standard deviation $\sigma_\theta = 2.0$.

```{code-cell} ipython3
# Set parameters
np.random.seed(123)
params_pi = PermIncomeModel(R=1.04, beta=1/1.04, sigma_psi=0.5, sigma_theta=2.0, T=80)
r = params_pi.R - 1

# Initialize
T = params_pi.T
b = np.zeros(T)
p = np.zeros(T)
y = np.zeros(T)
c = np.zeros(T)

b[0] = 0.0
p[0] = 50.0

# Generate shocks
psi = np.random.normal(0, params_pi.sigma_psi, T)
theta = np.random.normal(0, params_pi.sigma_theta, T)
psi[0] = 0  # No shock at t=0
theta[0] = 0

# Simulate
for t in range(T):
    if t > 0:
        p[t] = p[t-1] + psi[t]
    y[t] = p[t] + theta[t]
    c[t] = (r / params_pi.R) * (b[t] + theta[t]) + p[t]

    if t < T - 1:
        b[t+1] = (b[t] + y[t] - c[t]) * params_pi.R

# Plot
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(y, color='gray', alpha=0.5, lw=2, label='Income $y_t$')
ax.plot(p, color='blue', linestyle='--', lw=2, label='Permanent income $p_t$')
ax.plot(c, color='red', lw=2, label='Consumption $c_t$')
ax.set_xlabel('Time')
ax.set_ylabel('Value')
ax.set_title('Consumption Tracks Permanent Income')
ax.legend(frameon=False)
ax.grid(True, alpha=0.3)
plt.show()
```

Consumption tracks permanent income closely but barely responds to transitory fluctuations in income. When income spikes temporarily above permanent income, consumption rises only slightly, and the consumer saves most of the windfall. Conversely, when income dips temporarily, consumption is smoothed by drawing down savings.

### Code: Impulse Responses

We conduct two experiments to isolate the effects of permanent and transitory shocks. Each experiment starts from a steady state with no shocks, then introduces a unit shock at time $t = 10$.

```{code-cell} ipython3
# Impulse response simulation
np.random.seed(0)
T_ir = 40
shock_time = 10
r = 0.04
R = 1 + r

# Function to simulate impulse response
def impulse_response(shock_type='permanent', shock_size=1.0):
    b = np.zeros(T_ir)
    p = np.zeros(T_ir)
    y = np.zeros(T_ir)
    c = np.zeros(T_ir)

    # Initial steady state
    b[0] = 0.0
    p[0] = 50.0

    for t in range(T_ir):
        # Apply shock at shock_time
        psi_t = 0.0
        theta_t = 0.0

        if t == shock_time:
            if shock_type == 'permanent':
                psi_t = shock_size
            elif shock_type == 'transitory':
                theta_t = shock_size

        # Update permanent income
        if t > 0:
            p[t] = p[t-1] + psi_t

        # Observed income
        y[t] = p[t] + theta_t

        # Consumption function
        c[t] = (r / R) * (b[t] + theta_t) + p[t]

        # Update bank balance
        if t < T_ir - 1:
            b[t+1] = (b[t] + y[t] - c[t]) * R

    return y, p, c, b

# Run experiments
y_perm, p_perm, c_perm, b_perm = impulse_response('permanent')
y_trans, p_trans, c_trans, b_trans = impulse_response('transitory')

# Plot
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Permanent shock
axes[0, 0].plot(y_perm - 50, lw=2, label='Income', color='gray')
axes[0, 0].plot(c_perm - 50, lw=2, label='Consumption', color='red')
axes[0, 0].axvline(shock_time, color='black', linestyle=':', alpha=0.5)
axes[0, 0].set_xlabel('Time')
axes[0, 0].set_ylabel('Deviation from steady state')
axes[0, 0].set_title('Permanent Shock: Income and Consumption')
axes[0, 0].legend(frameon=False)
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].plot(b_perm, lw=2, color='blue')
axes[0, 1].axvline(shock_time, color='black', linestyle=':', alpha=0.5)
axes[0, 1].axhline(0, color='black', linestyle='-', alpha=0.3, lw=0.8)
axes[0, 1].set_xlabel('Time')
axes[0, 1].set_ylabel('Bank balance')
axes[0, 1].set_title('Permanent Shock: Bank Balance')
axes[0, 1].grid(True, alpha=0.3)

# Transitory shock
axes[1, 0].plot(y_trans - 50, lw=2, label='Income', color='gray')
axes[1, 0].plot(c_trans - 50, lw=2, label='Consumption', color='red')
axes[1, 0].axvline(shock_time, color='black', linestyle=':', alpha=0.5)
axes[1, 0].set_xlabel('Time')
axes[1, 0].set_ylabel('Deviation from steady state')
axes[1, 0].set_title('Transitory Shock: Income and Consumption')
axes[1, 0].legend(frameon=False)
axes[1, 0].grid(True, alpha=0.3)

axes[1, 1].plot(b_trans, lw=2, color='blue')
axes[1, 1].axvline(shock_time, color='black', linestyle=':', alpha=0.5)
axes[1, 1].axhline(0, color='black', linestyle='-', alpha=0.3, lw=0.8)
axes[1, 1].set_xlabel('Time')
axes[1, 1].set_ylabel('Bank balance')
axes[1, 1].set_title('Transitory Shock: Bank Balance')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

The permanent shock raises income and consumption by exactly one unit forever, with no change in bank balances. The consumer can afford to consume the full shock because it persists indefinitely. The transitory shock raises income by one unit for a single period. Consumption jumps by only $r/\mathsf{R} \approx 0.04$, and the consumer saves the rest. The bank balance becomes positive (the consumer accumulates assets), then gradually declines back to zero as the consumer slowly spends down the windfall.

### Why the Keynesian Consumption Function Fails

The estimated coefficient $\alpha_1$ in the regression $c_t = \alpha_0 + \alpha_1 y_t$ depends on the variance decomposition of income. If most income variation comes from transitory shocks, then $\hat{\alpha}_1 \approx r/\mathsf{R}$ (small). If most income variation comes from permanent shocks, then $\hat{\alpha}_1 \approx 1$ (large). The Keynesian consumption function conflates two distinct behavioral parameters into a single regression coefficient.

Hall's innovation was to test the theory via the random walk prediction instead. The unpredictability of consumption changes does not require specifying the income process or estimating how much of income variation is permanent versus transitory. The random walk implication holds regardless of the variance decomposition, as long as the consumer optimizes and $\mathsf{R}\beta = 1$.

### Exercises

```{exercise}
:label: ex_mpc_rates

Compute the transitory MPC $r/\mathsf{R}$ for interest rates $r \in \{0.02, 0.04, 0.06, 0.10\}$. Create a plot showing the transitory MPC as a function of $r$, and note that even at $r = 0.10$, the transitory MPC is only 0.091.
```

```{solution-start} ex_mpc_rates
:class: dropdown
```

```{code-cell} ipython3
r_grid = np.array([0.02, 0.04, 0.06, 0.10])
R_grid = 1 + r_grid
mpc_trans_grid = r_grid / R_grid

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(r_grid, mpc_trans_grid, marker='o', lw=2, color='darkblue')
ax.set_xlabel('Interest rate $r$')
ax.set_ylabel('Transitory MPC')
ax.set_title('Transitory MPC as a Function of Interest Rate')
ax.grid(True, alpha=0.3)
plt.show()

print("Interest rate | Transitory MPC")
print("-" * 30)
for r_val, mpc_val in zip(r_grid, mpc_trans_grid):
    print(f"   {r_val:.2f}      |     {mpc_val:.4f}")
```

Even when the interest rate is 10 percent, the transitory MPC is only 0.091. The consumer consumes roughly one-tenth of a transitory windfall and saves the rest.

```{solution-end}
```

```{exercise}
:label: ex_unpredictable

Simulate a consumer facing a predictable income process: income grows deterministically by $\Delta y = 1$ every period, plus small transitory noise with standard deviation $\sigma_\theta = 0.5$. Simulate for $T = 50$ periods starting from $b_0 = 0$ and $p_0 = 50$. Plot income and consumption over time. Show that income changes are predictable (they grow by approximately 1 each period), but consumption changes remain unpredictable.
```

```{solution-start} ex_unpredictable
:class: dropdown
```

```{code-cell} ipython3
np.random.seed(999)
T_pred = 50
r = 0.04
R = 1 + r

b_pred = np.zeros(T_pred)
p_pred = np.zeros(T_pred)
y_pred = np.zeros(T_pred)
c_pred = np.zeros(T_pred)

b_pred[0] = 0.0
p_pred[0] = 50.0

# Deterministic permanent income growth
for t in range(T_pred):
    if t > 0:
        p_pred[t] = p_pred[t-1] + 1.0  # Deterministic growth

    theta_t = np.random.normal(0, 0.5)
    y_pred[t] = p_pred[t] + theta_t
    c_pred[t] = (r / R) * (b_pred[t] + theta_t) + p_pred[t]

    if t < T_pred - 1:
        b_pred[t+1] = (b_pred[t] + y_pred[t] - c_pred[t]) * R

# Compute changes
delta_y_pred = np.diff(y_pred)
delta_c_pred = np.diff(c_pred)

# Plot
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].plot(y_pred, lw=2, label='Income $y_t$', color='gray')
axes[0].plot(c_pred, lw=2, label='Consumption $c_t$', color='red')
axes[0].set_xlabel('Time')
axes[0].set_ylabel('Value')
axes[0].set_title('Predictable Income Growth')
axes[0].legend(frameon=False)
axes[0].grid(True, alpha=0.3)

axes[1].plot(delta_y_pred, lw=2, label='$\\Delta y_t$', color='gray', alpha=0.7)
axes[1].plot(delta_c_pred, lw=2, label='$\\Delta c_t$', color='red')
axes[1].axhline(1, color='black', linestyle='--', alpha=0.5, label='Expected $\\Delta y = 1$')
axes[1].set_xlabel('Time')
axes[1].set_ylabel('Change')
axes[1].set_title('Income Changes (Predictable) vs Consumption Changes (Not)')
axes[1].legend(frameon=False)
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print(f"Mean income change: {np.mean(delta_y_pred):.3f}")
print(f"Mean consumption change: {np.mean(delta_c_pred):.3f}")
print(f"Std dev of income change: {np.std(delta_y_pred):.3f}")
print(f"Std dev of consumption change: {np.std(delta_c_pred):.3f}")
```

Income changes are predictable (they average approximately 1), but consumption changes remain close to zero on average. The consumer smooths consumption optimally by anticipating the deterministic income growth.

```{solution-end}
```

```{exercise}
:label: ex_impulse_confused

Consider a consumer who cannot distinguish permanent from transitory shocks. The consumer observes total income $y_t$ but not the separate components $p_t$ and $\theta_t$. Suppose the consumer treats every income change as having fraction $\lambda = 0.5$ permanent and fraction $1 - \lambda = 0.5$ transitory. Simulate the response to a unit permanent shock at $t = 10$ when the consumer uses this rule, and compare to the optimal response (from the earlier impulse response plot). Show that consumption under-reacts initially and adjusts gradually over time as the consumer learns the shock is permanent.
```

```{solution-start} ex_impulse_confused
:class: dropdown
```

```{code-cell} ipython3
np.random.seed(42)
T_conf = 40
shock_time_conf = 10
r = 0.04
R = 1 + r
lambda_mix = 0.5

# Optimal (fully informed) consumer
b_opt = np.zeros(T_conf)
p_true = np.zeros(T_conf)
y_opt = np.zeros(T_conf)
c_opt = np.zeros(T_conf)

p_true[0] = 50.0

for t in range(T_conf):
    if t == shock_time_conf:
        p_true[t] = p_true[t-1] + 1.0
    elif t > shock_time_conf:
        p_true[t] = p_true[t-1]

    y_opt[t] = p_true[t]
    c_opt[t] = (r / R) * b_opt[t] + p_true[t]

    if t < T_conf - 1:
        b_opt[t+1] = (b_opt[t] + y_opt[t] - c_opt[t]) * R

# Confused consumer (treats shock as mixed)
b_conf = np.zeros(T_conf)
p_perceived = np.zeros(T_conf)
y_conf = np.zeros(T_conf)
c_conf = np.zeros(T_conf)

p_perceived[0] = 50.0

for t in range(T_conf):
    # True income includes permanent shock at t=10
    if t == shock_time_conf:
        income_shock = 1.0
    else:
        income_shock = 0.0

    if t > 0:
        # Consumer perceives lambda of the income change as permanent
        delta_y = y_conf[t-1] + income_shock - y_conf[t-1] if t == shock_time_conf else 0.0
        if t == shock_time_conf:
            p_perceived[t] = p_perceived[t-1] + lambda_mix * 1.0
        else:
            p_perceived[t] = p_perceived[t-1]

    # True income (contains permanent shock at t=10)
    if t >= shock_time_conf:
        y_conf[t] = 51.0
    else:
        y_conf[t] = 50.0

    # Consumer's consumption decision based on perceived permanent income
    # and treating (1-lambda) of shock as transitory
    if t == shock_time_conf:
        theta_perceived = (1 - lambda_mix) * 1.0
    else:
        theta_perceived = 0.0

    c_conf[t] = (r / R) * (b_conf[t] + theta_perceived) + p_perceived[t]

    if t < T_conf - 1:
        b_conf[t+1] = (b_conf[t] + y_conf[t] - c_conf[t]) * R

# Plot comparison
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(c_opt - 50, lw=2, label='Optimal (fully informed)', color='blue')
ax.plot(c_conf - 50, lw=2, label='Confused ($\\lambda = 0.5$)', color='orange', linestyle='--')
ax.axvline(shock_time_conf, color='black', linestyle=':', alpha=0.5)
ax.axhline(1, color='blue', linestyle=':', alpha=0.5, label='Full permanent response')
ax.set_xlabel('Time')
ax.set_ylabel('Consumption deviation from steady state')
ax.set_title('Response to Permanent Shock: Optimal vs Confused Consumer')
ax.legend(frameon=False)
ax.grid(True, alpha=0.3)
plt.show()

print(f"Optimal consumption jump at t={shock_time_conf}: {c_opt[shock_time_conf] - c_opt[shock_time_conf-1]:.4f}")
print(f"Confused consumption jump at t={shock_time_conf}: {c_conf[shock_time_conf] - c_conf[shock_time_conf-1]:.4f}")
print(f"Confused consumer initially consumes {lambda_mix:.1%} of optimal response")
```

The confused consumer under-reacts to the permanent shock, initially raising consumption by only $\lambda + (1-\lambda) \cdot r/\mathsf{R} \approx 0.52$ instead of the full 1.0. The consumer accumulates unintended savings (bank balance rises), which gradually finances additional consumption over time. Full adjustment occurs slowly as the consumer realizes the shock persists.

```{solution-end}
```

## References

```{bibliography}
:filter: docname in docnames
```
