# Phase 2 — Budget Contingency Tree

**Version:** 1.0
**Date:** 2026-03-13

---

## Purpose

Pre-approve three pilot scopes so that when lab quotes arrive, we negotiate against a real decision tree instead of improvising.

---

## Scope A: Full Validation (preferred)

**Design:** 45 devices = 3 families × 3 recipes × 5 replicates
**Budget range:** $15K–$50K (single-lab to two-partner)

| Component | Single-lab | Two-partner |
|-----------|-----------|-------------|
| Fabrication (45 devices) | $6K–$13K | $6K–$13K |
| Indoor stability (MPP + JV) | $4K–$10K | $6K–$14K |
| Post-mortem (~18 outlier devices) | $2K–$5K | $3K–$6K |
| Metadata/blinding overhead | $1K–$3K | $2K–$4K |
| Contingency (10%) | $1.5K–$3K | $2K–$4K |
| **Total** | **$15K–$35K** | **$25K–$50K** |

**What it proves:** Decisive within-family validation. Publishable. Clear pass/fail.
**Decision power:** High — designed to be conclusive.

---

## Scope B: Reduced Validation (fallback)

**Design:** 30 devices = 3 families × 2 recipes (model-favored + baseline) × 5 replicates
**Budget range:** $10K–$25K

**What's cut:** Negative controls removed. Saves ~33% on fabrication and testing.
**What's preserved:** Pairwise model-favored vs baseline comparison. Blinding. Metadata.
**What's lost:** Cannot test whether model correctly identifies *bad* recipes. Weaker falsification.

| Adjusted pass/fail |
|--------------------|
| PASS: Model-favored beats baseline median T80 in ≥2/3 families (by ≥10%) |
| FAIL: No lift in any family |
| Note: Without negative controls, a "pass" is weaker evidence — the model might rank well at the top but poorly overall |

**When to choose this:** Lab quotes come in above $35K for full scope, and no second lab is available at reasonable cost.

---

## Scope C: Feasibility Screen (minimum viable pilot)

**Design:** 15–20 devices = 1–2 families × 2 recipes × 4–5 replicates
**Budget range:** $5K–$12K

**What's cut:** One or two families dropped. Possibly fewer replicates.
**What's preserved:** Blinding, metadata capture, MPP tracking, analysis pipeline dry-run.
**What's lost:** Statistical power. NOT a decisive validation.

**This scope is explicitly labeled non-decisive.** Its purpose is to:
1. Test logistics (metadata completeness, raw data quality, blinding fidelity)
2. Validate the intake pipeline (CSV validator, analysis script, deviation rules)
3. Generate preliminary signal for fundraising or expanded pilot
4. De-risk Scope A by catching process/logistics problems early

| Adjusted pass/fail |
|--------------------|
| No formal pass/fail for the model. Instead, evaluate: |
| - Did metadata capture achieve ≥90% completeness? |
| - Did blinding hold? |
| - Did MPP data arrive in usable format? |
| - Is there any directional signal (even if underpowered)? |

**When to choose this:** Budget below $12K, or partner can only do 1–2 families under fixed stack, or we want a logistics dry-run before committing to full scope.

---

## Decision tree when quotes arrive

```
Quote ≤ $35K for full scope (single-lab)?
  YES → Execute Scope A (single-lab)
  NO  →
    Quote ≤ $50K for two-partner?
      YES → Execute Scope A (two-partner, preferred)
      NO  →
        Quote ≤ $25K for reduced scope?
          YES → Execute Scope B (reduced validation)
          NO  →
            Quote ≤ $12K for feasibility?
              YES → Execute Scope C (feasibility screen)
              NO  → Seek alternative lab or funding
```

## What each scope enables afterward

| Scope | If positive | If negative |
|-------|------------|-------------|
| A (full) | Publish. Expand families. Scope Phase 3. | Publish negative. Pivot to mechanism program. |
| B (reduced) | Cautious claim. Seek funding for full validation. | Pivot to mechanism program. |
| C (feasibility) | De-risked logistics. Seek funding for Scope A/B. | Identify what broke. Fix before retry. |

---

*Pre-approve scope selection criteria before outreach begins. Do not negotiate scope under pressure during partner conversations.*
