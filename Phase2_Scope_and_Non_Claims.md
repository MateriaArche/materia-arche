# Materia Arche — Phase 2 Scope and Non-Claims

**Version:** 1.0
**Date:** 2026-03-12
**Status:** Pre-registration draft

---

## What this pilot validates

This Phase 2 pilot is a **blinded, prospective, within-family validation** of a frozen ranking model under a fixed ageing protocol.

Specifically, we test the claim:

> For a given composition family and device architecture, the model can rank fabrication recipes by stability better than baseline lab choice.

The primary metric is **pairwise within-family win rate**: how often does the model-favored recipe outlast the baseline recipe within the same composition family?

## What this pilot does NOT validate

- **Cross-family superiority.** The model cannot reliably predict whether FA-Cs is more stable than MAPbI₃. Leave-one-group-out CV tau-b = 0.005 (P-037). This pilot does not test cross-family claims.

- **Mechanism or causation.** The model ranks by statistical correlation with fabrication/process features. It does not explain *why* a recipe is more stable. Mechanism understanding is a separate R&D program.

- **Temporal generalization.** The model was trained on literature data through a fixed cutoff. Temporal holdout tau-b = 0.11–0.13 (P-035, P-048). Performance on future fabrication methods is not guaranteed.

- **Quantum advantage.** Quantum computing experiments (9 tested, 0 positive lift) are a separate R&D track, not an execution gate for this pilot.

## Model scope

| Property | Value |
|----------|-------|
| Algorithm | ExtraTreesRegressor (frozen config) |
| Features | 31 (kitchen sink: composition + fabrication + process) |
| Target | log1p(Stability_PCE_T80) — used for ranking only |
| Training data | 1,543 devices from Perovskite Database (frozen snapshot) |
| Uncertainty | Split conformal prediction intervals (80% nominal coverage) |
| Validated for | Within-family ranking (tau-b 0.27–0.34 depending on family) |
| Not validated for | Cross-family comparison, temporal extrapolation |

## Evidence base

48 work packets (P-001 through P-048):
- 23 Confirmed, 13 Negative, 8 Promising
- Credibility ratio: 60.8% (P-044)
- Full evidence: [GitHub](https://github.com/MateriaArche/materia-arche) and [Google Drive](https://drive.google.com/drive/folders/1b2zZAfkEcxQH6TERfDJ-YCb1uvEo-TEz)

Key findings that define scope:
- P-037: LOGO tau-b = 0.005 (cross-family generalization fails)
- P-042: Panel devices top-20 within own family 100% of time
- P-046: Fabrication features (solvents, layers) give +0.040 tau-b lift
- P-047: Panel survives 31-feature model upgrade

## How to cite limitations

In any partner communication, outreach, or publication, include:

> "This model is validated as a within-family fabrication-quality ranker. It does not predict cross-family stability differences. See Phase2_Scope_and_Non_Claims.md for full details."

---

*This document is part of the frozen artifact set for Phase 2. Do not modify after pilot launch.*
