# Phase 2 — Pre-Registered Test Matrix

**Version:** 1.0
**Date:** 2026-03-12
**Status:** Draft — to be frozen before pilot launch

---

## Design rationale

The pilot tests **within-family ranking**, not cross-family comparison (see Phase2_Scope_and_Non_Claims.md).

For each composition family, we fabricate three recipes:
- **Model-favored:** Highest-ranked recipe by the frozen model
- **Baseline:** Standard lab recipe (lab's default for that family)
- **Negative control:** Low-ranked recipe by the frozen model

This gives a falsifiable pairwise test: does the model's top pick beat baseline, and does baseline beat the model's bottom pick?

## Test matrix

### Family 1: Pure MA (MAPbI₃)
| Recipe | Source | Replicates | Total devices |
|--------|--------|------------|---------------|
| Model-favored (based on Device 850 profile) | Model rank #1 within Pure MA | 5 | 5 |
| Baseline | Lab standard MAPbI₃ recipe | 5 | 5 |
| Negative control | Model rank bottom-20% within Pure MA | 5 | 5 |
| **Subtotal** | | | **15** |

### Family 2: MA-FA Mixed
| Recipe | Source | Replicates | Total devices |
|--------|--------|------------|---------------|
| Model-favored (based on Device 1320 profile) | Model rank #1 within MA-FA | 5 | 5 |
| Baseline | Lab standard MA-FA recipe | 5 | 5 |
| Negative control | Model rank bottom-20% within MA-FA | 5 | 5 |
| **Subtotal** | | | **15** |

### Family 3: FA-Cs
| Recipe | Source | Replicates | Total devices |
|--------|--------|------------|---------------|
| Model-favored (based on Device 119 profile) | Model rank #1 within FA-Cs | 5 | 5 |
| Baseline | Lab standard FA-Cs recipe | 5 | 5 |
| Negative control | Model rank bottom-20% within FA-Cs | 5 | 5 |
| **Subtotal** | | | **15** |

### Total: 45 devices (9 recipes × 5 replicates)

## Constraints

All 45 devices share:
- **Same substrate** (specified by lab)
- **Same device architecture** (e.g., n-i-p or p-i-n — lab's standard)
- **Same encapsulation** (material and method fixed)
- **Same active area** (lab's standard cell size)
- **Same ageing protocol** (one ISOS category, fixed before fabrication)
- **Same measurement equipment** (same solar simulator, same MPP tracker)

The **only intentional variable** within each family is the fabrication recipe (solvent ratios, annealing conditions, layer thicknesses, deposition parameters).

## Blinding protocol

1. Model generates ranked recipe list per family before pilot starts
2. Recipes are assigned blinded IDs (e.g., F1-A, F1-B, F1-C)
3. Lab receives recipes as blinded fabrication instructions
4. Lab does not know which is model-favored, baseline, or negative control
5. Ageing and measurement proceed under blinded IDs
6. Unblinding occurs only after all T80/MPP data is collected and locked

## Fabrication order

- Randomized within each family
- All replicates of one recipe fabricated in the same batch (to control batch-to-batch variance)
- Fabrication order logged with timestamps

## Primary endpoint

**Pairwise within-family win rate:**

For each family, compare median T80:
- Model-favored vs Baseline → Win / Loss / Tie
- Baseline vs Negative control → Win / Loss / Tie

A "win" requires the favored recipe's median T80 to exceed the comparator by ≥10% (to avoid noise-driven claims).

## Secondary endpoints

1. **Conformal interval calibration:** Do the model's 80% prediction intervals cover ~77–80% of observed T80 values? (Baseline from P-039)
2. **Rank correlation:** Kendall tau-b between model-predicted rank and observed T80 within each family
3. **Degradation curve shape:** Do model-favored recipes show different degradation profiles (burn-in, linear, exponential)?
4. **Post-mortem patterns:** Do failure modes differ between model-favored and negative control recipes?

## Pass/fail gates

### PASS
- Model-favored beats baseline median T80 in **≥2 of 3 families** (by ≥10%)
- Pairwise within-family win rate **≥65%** across all comparisons
- Conformal intervals not obviously miscalibrated (coverage 60–90%)
- No major protocol deviations

### PARTIAL PASS
- 1 family clear win, 1 ambiguous, 1 fail
- Good metadata completeness (≥90% of critical fields)
- Sufficient raw data to retrain family-specific models

### FAIL
- No clear within-family lift in any family
- Large protocol drift or missing process metadata (>20% missing critical fields)
- Results only explainable by batch-to-batch or lab-to-lab variance

## Decision tree after pilot

| Outcome | Next action |
|---------|-------------|
| PASS | Publish results. Expand to 2–3 additional families. Scope Phase 3 scale-up. |
| PARTIAL PASS | Analyze which family failed and why. Retrain family-specific model with pilot data. Run focused follow-up on failing family. |
| FAIL | Publish negative result honestly. Pivot to mechanism-labeling program. Shelve ranking model until better data exists. |

## Budget estimate

| Item | Estimate |
|------|----------|
| Substrate + materials (45 devices) | $2,000–$4,000 |
| Fabrication labor | $3,000–$6,000 |
| Ageing/characterization (500+ hours MPP) | $2,000–$5,000 |
| Post-mortem (PL/EL/XRD on ~18 outlier devices) | $1,000–$3,000 |
| **Total** | **$8,000–$18,000** |

## Frozen artifacts (must be locked before fabrication begins)

| Artifact | Format | Hash |
|----------|--------|------|
| Model binary | pickle | TBD at freeze |
| Training data snapshot | CSV | TBD at freeze |
| Feature list (31 features) | text | TBD at freeze |
| Recipe selection script | .py | TBD at freeze |
| Conformal calibration parameters | JSON | TBD at freeze |
| This test matrix | .md | TBD at freeze |
| Scope and non-claims | .md | TBD at freeze |
| Metadata template | .md | TBD at freeze |
| Analysis script | .py | TBD at freeze |

All hashes computed at freeze time and recorded in a signed manifest.

---

*This document will be frozen (version-locked with git hash) before any lab partner is contacted.*
