# Phase 2 — Negative Result Templates

**Version:** 1.0
**Date:** 2026-03-13

Pre-written templates for each failure mode. Having these ready before data lands keeps us honest.

---

## Template 1: No lift in any family (FAIL)

> **Result:** The frozen within-family ranking model did not demonstrate predictive lift over baseline lab choice in any of the three composition families tested.
>
> **Details:** Model-favored recipes did not outperform baseline recipes by the pre-registered ≥10% median T80 threshold in Pure MA, MA-FA mixed, or FA-Cs. Pairwise win rate was X% (threshold: 65%).
>
> **Interpretation:** The model's within-family ranking signal, validated at tau-b 0.27–0.34 on retrospective data, did not transfer to prospective fabrication. Possible explanations: (1) lab-to-lab variance dominates recipe differences, (2) model learned dataset-specific correlations not present in this lab's process, (3) recipe transfer introduced uncontrolled variables.
>
> **Next step:** Publish negative result. Investigate whether metadata reveals systematic lab-vs-model discrepancies. Consider feasibility screen at the same lab with model retrained on their process data.

---

## Template 2: Lift in one family only (PARTIAL PASS)

> **Result:** The model demonstrated within-family ranking lift in [FAMILY] (median T80 improvement X%, p=Y) but not in [FAMILY_2] or [FAMILY_3].
>
> **Details:** Pairwise win rate was X% overall. The successful family had N devices with Z% metadata completeness. The unsuccessful families showed [describe pattern].
>
> **Interpretation:** The model's ranking signal is real but family-dependent, consistent with the retrospective finding that within-family tau-b varies from 0.024 (Pure FA) to 0.40 (Triple cation). The successful family may have had more training data representation or more process-sensitive stability.
>
> **Next step:** Retrain family-specific model using pilot data from the successful family. Run focused follow-up on one unsuccessful family with adjusted recipe selection. Do not claim general validation.

---

## Template 3: Lift but bad metadata compliance (PARTIAL PASS / FAIL)

> **Result:** Model-favored recipes showed directional improvement in X/3 families, but metadata completeness was only Y% (threshold: 80%), with Z critical fields systematically missing.
>
> **Details:** [List missing fields and pattern]. The missing data prevents confident attribution of stability differences to recipe choices vs. uncontrolled variables.
>
> **Interpretation:** The pilot's execution quality was insufficient to draw conclusions about model validity. This is a logistics failure, not a model failure.
>
> **Next step:** Treat as feasibility screen. Fix metadata capture protocol. Re-run with stricter process control and complete metadata before claiming validation.

---

## Template 4: Lift disappears under deviation exclusions (FAIL)

> **Result:** Before exclusions, model-favored recipes appeared to outperform baseline in X/3 families. After applying pre-registered exclusion rules, the lift was no longer statistically meaningful.
>
> **Details:** N devices excluded for [reasons]. Remaining sample size was insufficient for the pre-registered statistical test. Exclusion rate X% [above/below] the 20% threshold.
>
> **Interpretation:** The apparent lift was driven by devices that failed quality control. The model's ranking signal does not survive data cleaning.
>
> **Next step:** Investigate whether excluded devices share a systematic pattern (e.g., all from one batch, all one operator). If exclusions are random, increase sample size. If systematic, fix the process first.

---

## Template 5: Conformal intervals badly miscalibrated (secondary finding)

> **Result:** The model's 80% conformal prediction intervals covered only X% of observed T80 values (acceptable range: 60–90%).
>
> **Details:** [Over-coverage / under-coverage] was most pronounced in [family/regime]. The calibration parameters were computed on retrospective data (q-hat = Y) and may not transfer to this lab's process distribution.
>
> **Interpretation:** The uncertainty estimates need recalibration on prospective data. The ranking signal should be evaluated independently of interval calibration.
>
> **Next step:** Recompute conformal parameters using pilot data as the new calibration set. Report recalibrated intervals alongside original.

---

*These templates exist to prevent post-hoc rationalization. Use the template that fits, edit only the factual details, and publish the result regardless of outcome.*
