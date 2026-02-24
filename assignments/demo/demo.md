---
jupytext:
  formats: md:myst,ipynb
  cell_metadata_filter: nbgrader,-all
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.18.1
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Demo: How nbgrader Notebooks Work

Welcome to the course assignments! This short demo walks you through the three types of cells you will encounter, then gives you three quick practice exercises (15 points total) so you can verify that your setup works before tackling the real assignments.

## How this notebook works

Every assignment notebook contains three kinds of cells:

1. **Read-only cells** (locked, gray background). These load packages, define parameters, or set up the problem. Do not modify them.
2. **Solution cells**. These contain the placeholder `# YOUR CODE HERE` followed by `raise NotImplementedError()`. Delete both lines and replace them with your code. Keep the function signature and variable names exactly as given.
3. **Test cells** (locked). Some assertions are visible so you can check your work locally. Additional hidden tests run on the autograder server and are worth the bulk of the points.

**Before submitting**, always run **Kernel → Restart & Run All** to make sure every cell executes from a clean state.

## Setup

```{code-cell} ipython3
---
nbgrader:
  grade: false
  grade_id: setup
  locked: true
  schema_version: 3
  solution: false
  task: false
---
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = (8, 5)
plt.rcParams['font.size'] = 11
```

## Exercise 1: Compound interest (5 points)

A principal $P$ invested at annual interest rate $r$ for $t$ years grows to

$$A = P(1 + r)^{t}.$$

Implement a function that returns the future value $A$.

```{code-cell} ipython3
---
nbgrader:
  grade: false
  grade_id: ex_1
  locked: false
  schema_version: 3
  solution: true
  task: false
---
def compound_interest(P, r, t):
    """Return the future value of principal P at rate r after t years."""
    ### BEGIN SOLUTION
    return P * (1 + r) ** t
    ### END SOLUTION


# Quick sanity check
print(f"$100 at 5% for 10 years = ${compound_interest(100, 0.05, 10):.2f}")
```

```{code-cell} ipython3
---
nbgrader:
  grade: true
  grade_id: test_1_visible
  locked: true
  points: 3
  schema_version: 3
  solution: false
  task: false
---
# Autograder tests for Exercise 1 (visible)
assert callable(compound_interest), "compound_interest must be a function"
assert np.isclose(compound_interest(100, 0.05, 0), 100), "With t=0 the principal should be unchanged"
assert np.isfinite(compound_interest(100, 0.05, 10)), "Result should be finite"
```

```{code-cell} ipython3
---
nbgrader:
  grade: true
  grade_id: test_1_hidden
  locked: true
  points: 2
  schema_version: 3
  solution: false
  task: false
---
### BEGIN HIDDEN TESTS
assert np.isclose(compound_interest(100, 0.05, 10), 100 * 1.05**10), \
    "compound_interest(100, 0.05, 10) is incorrect"
assert np.isclose(compound_interest(1, 0.10, 1), 1.10), \
    "compound_interest(1, 0.10, 1) should be 1.10"
assert np.isclose(compound_interest(500, 0.0, 20), 500), \
    "Zero interest rate should leave principal unchanged"
### END HIDDEN TESTS
```

## Exercise 2: Present discounted value (5 points)

The present discounted value of a stream of cash flows $C_0, C_1, \ldots, C_{T-1}$ at discount rate $r$ is

$$\text{PDV} = \sum_{t=0}^{T-1} \frac{C_t}{(1+r)^{t}}.$$

Implement a function that takes an array of cash flows and returns the PDV.

```{code-cell} ipython3
---
nbgrader:
  grade: false
  grade_id: ex_2
  locked: false
  schema_version: 3
  solution: true
  task: false
---
def pdv(cashflows, r):
    """Return the present discounted value of a cashflow array at rate r."""
    ### BEGIN SOLUTION
    cashflows = np.asarray(cashflows, dtype=float)
    t = np.arange(len(cashflows))
    return np.sum(cashflows / (1 + r) ** t)
    ### END SOLUTION


# Quick sanity check
print(f"PDV of [100, 100, 100] at r=0.05: ${pdv([100, 100, 100], 0.05):.2f}")
```

```{code-cell} ipython3
---
nbgrader:
  grade: true
  grade_id: test_2_visible
  locked: true
  points: 2
  schema_version: 3
  solution: false
  task: false
---
# Autograder tests for Exercise 2 (visible)
assert callable(pdv), "pdv must be a function"
assert np.isclose(pdv([100], 0.05), 100), "A single cash flow at t=0 should equal itself"
assert np.isfinite(pdv([100, 100, 100], 0.05)), "Result should be finite"
```

```{code-cell} ipython3
---
nbgrader:
  grade: true
  grade_id: test_2_hidden
  locked: true
  points: 3
  schema_version: 3
  solution: false
  task: false
---
### BEGIN HIDDEN TESTS
assert np.isclose(pdv([100, 100, 100], 0.05), 100 + 100/1.05 + 100/1.05**2), \
    "PDV of [100, 100, 100] at r=0.05 is incorrect"
assert np.isclose(pdv([0, 0, 200], 0.10), 200 / 1.10**2), \
    "PDV of [0, 0, 200] at r=0.10 is incorrect"
assert np.isclose(pdv(np.ones(5) * 50, 0.0), 250.0), \
    "At r=0 the PDV should be the simple sum"
### END HIDDEN TESTS
```

## Exercise 3: Plot a budget constraint (5 points)

A consumer earns income $Y$ in period 1 (and zero in period 2) and can save or borrow at gross interest rate $R = 1 + r$. The budget constraint in period 2 is

$$c_2 = (Y - c_1) \cdot R.$$

Compute two arrays:
- `c1_vals`: 200 evenly spaced values from 0 to $Y$ (inclusive)
- `c2_vals`: the corresponding period-2 consumption from the budget constraint

Then plot the budget line.

```{code-cell} ipython3
---
nbgrader:
  grade: false
  grade_id: ex_3
  locked: false
  schema_version: 3
  solution: true
  task: false
---
# Parameters (do not change)
Y = 100     # period-1 income
R = 1.05    # gross interest rate

### BEGIN SOLUTION
c1_vals = np.linspace(0, Y, 200)
c2_vals = (Y - c1_vals) * R
### END SOLUTION

# Plot the budget constraint
plt.plot(c1_vals, c2_vals)
plt.xlabel('Period 1 consumption ($c_1$)')
plt.ylabel('Period 2 consumption ($c_2$)')
plt.title('Intertemporal budget constraint')
plt.grid(True, alpha=0.3)
plt.show()
```

```{code-cell} ipython3
---
nbgrader:
  grade: true
  grade_id: test_3_visible
  locked: true
  points: 2
  schema_version: 3
  solution: false
  task: false
---
# Autograder tests for Exercise 3 (visible)
assert len(c1_vals) == len(c2_vals), "c1_vals and c2_vals must have the same length"
assert np.all(c1_vals >= 0), "c1_vals should be non-negative"
assert np.all(c2_vals >= -1e-10), "c2_vals should be non-negative along the budget line"
```

```{code-cell} ipython3
---
nbgrader:
  grade: true
  grade_id: test_3_hidden
  locked: true
  points: 3
  schema_version: 3
  solution: false
  task: false
---
### BEGIN HIDDEN TESTS
assert len(c1_vals) == 200, "c1_vals should have 200 elements"
assert np.isclose(c1_vals[0], 0.0), "c1_vals should start at 0"
assert np.isclose(c1_vals[-1], 100.0), "c1_vals should end at 100"
assert np.isclose(c2_vals[0], 100.0 * 1.05), "When c1=0, c2 should equal 105"
assert np.isclose(c2_vals[-1], 0.0), "When c1=Y, c2 should equal 0"
### END HIDDEN TESTS
```

## Submission

1. Re-run the entire notebook: **Kernel → Restart & Run All**
2. Verify that every cell executes without errors
3. Save the notebook
4. Upload the `.ipynb` file to Gradescope
