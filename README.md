**Agent Operating System:** [MATERIA_ARCHE_AGENT_OS_v3.0.md](MATERIA_ARCHE_AGENT_OS_v3.0.md)

**Important:** Please read [Honesty Note](README_Honesty_Note.md) first.

# Materia Arche

ML-orchestrated stability prediction for perovskite solar cells.

## What this is

An end-to-end pipeline that ranks perovskite compositions by predicted T80 stability, validated against 1,543 devices from the Perovskite Database Project.

- **Best model:** ExtraTreesRegressor — Kendall tau-b 0.271 (CV 0.289)
- **Classical baseline lift:** +0.155 over composition-only ranking
- **SHAP top drivers:** Jsc, bandgap, Voc
- **Quantum experiments:** 9 tested, 0 positive lift (closed as research track)
- **Lab panel:** 3 diversified, perturbation-robust candidates locked via P-005→P-010, E4 validation-ready
- **Work packets:** 30 closed (P-001 through P-030), 14 Confirmed, 6 Negative, 4 Promising

## Notebooks

| # | Notebook | What it does |
|---|----------|-------------|
| 01 | Data preparation | Load and clean Perovskite Database, extract T80 stability |
| 02 | ML baseline | Random Forest baseline (tau-b 0.249) |
| 03 | Candidate shortlist | Rank compositions, identify candidates |
| 04 | Ablation & evidence | Feature importance, ablation study |
| 05 | Phase 2 preparation | Lab scoping, decision framework |
| 06 | Outreach package v1 | Draft outreach templates |
| 07 | Lab quotes & evidence | Lab cost estimates, evidence packaging |
| 08 | Quantum diagnostics | Diagnose quantum feature failure (6 experiments) |
| 09 | Quantum re-test | Trained variational circuit, milestone re-eval |
| 10 | VQE experiment | Per-device VQE energy, 9th experiment fails |
| 11 | Decision gate | Close quantum track, present Options A/B/C |
| 12 | Phase 2 outreach | Final outreach templates, lab scoping table |
| 13 | ML variation sweep | 4 models x 30 configs — ExtraTrees wins |
| 14 | Deepen winner | Feature engineering, ensemble tests |
| 15 | Final ML push | Grid search, bootstrap CIs, production model locked |
| 16 | Nitrogen roadmap | What nitrogen fixation ML actually needs |
| 17 | SHAP + lab panel | SHAP analysis, 3-candidate selection for Phase 2 |
| 18 | P-001 Reproducibility | 20-split reproducibility audit of locked ET model |
| 19 | P-002 Variance reduction | 4 strategies tested — variance is structural |
| 20 | P-003 Uncertainty ranking | Per-tree prediction intervals, 1/10 separated |
| 21 | P-004 Shortlist robustness | Frozen top-3 not stable across splits |
| 22 | P-005 Robust lab panel | New 3-candidate panel via test-set-only ranking |
| 23 | P-006 Panel profiling | Composition diversity check — all MA-only, needs diversification |
| 24 | P-007 Diversified panel lock | 3 families, all 100% top-20 rate — E4 validation-ready |
| 25 | P-008 Phase 2 outreach package | Complete partner-ready package with protocol and budget |
| 26 | Full pipeline summary audit | End-to-end audit: dataset → model → 8 packets → locked panel |
| 27 | P-009 Perturbation sensitivity | Feature noise ±1–20%, Device 1064 fragile at 10% |
| 28 | P-010 Panel replacement | Device 1320 replaces 1064 — all 3 now 100% noise-robust |
| 29 | P-011 Multi-model consensus | GradientBoosting disagrees on 2/3 panel devices — Negative |
| 30 | P-012 Learning curve | +0.051 tau-b per doubling, not saturated — Promising |
| 31 | P-013 Publication bias | LOGO CV tau-b 0.055 vs random 0.289 — Negative (composition-cluster dependent) |
| 32 | P-014 Feature interactions | Top: Voc×FF (H=5.03), area×Jsc — physically meaningful, Confirmed |
| 33 | P-015 Interval calibration | 80% PI covers only 66% — under-covers, especially long-lived devices, Negative |
| 34 | P-016 Novel composition holdout | LOFO tau-b 0.005 — model doesn't generalize to unseen families, Negative |
| 35 | P-017 Conformal calibration | Fixes P-015: 80% PI now covers 79.9%, Confirmed |
| 36 | P-018 Feature importance stability | NB17 top-3 (Jsc/bandgap/Voc) not stable — actual: bandgap/area/thickness, Negative |
| 37 | P-019 High-confidence consensus | 31% of devices in multi-model agreement zone, tau-b 0.346, Promising |
| 38 | P-020 Corrected feature importance | 6 consensus top-5 features across 3 methods, bandgap most stable, Confirmed |
| 39 | P-021 Hyperparameter sensitivity | Panel 100% top-20 across all 25 ET configs tested, Confirmed |
| 40 | P-022 Full pipeline audit v2 | 21-packet ledger, 12 Confirmed, credibility 57%, Confirmed |
| 41 | P-023 Missingness impact | Dropping 65%-missing features loses <0.02 tau-b, Promising |
| 42 | P-024 Target leakage audit | No leakage — all features measured before/during fabrication, Confirmed |
| 43 | P-025 Reduced-feature model | 14-feature clean model: -0.012 tau-b, panel 100%, Confirmed |
| 44 | P-026 Ensemble stacking | Stacking ET+RF+GB doesn't beat ET alone (-0.005), Negative |
| 45 | P-027 Bootstrap CI on tau-b | 95% CI entirely above 0.15 — predictive power confirmed, Confirmed |
| 46 | P-028 Residual analysis | Systematic underprediction of long-lived devices, no family bias, Promising |
| 47 | P-029 Updated outreach package | Revised partner brief v2 with 28-packet findings, Confirmed |
| 48 | P-030 Model card | Mitchell et al. format, full transparency documentation, Confirmed |

## Current status

- **Perovskite:** Phase 2 ACTIVE — production model locked, noise-robust lab panel confirmed (P-010)
- **Lab panel:** 3 compositions across 3 families, all 100% top-20 rate at ±10% noise — E4 validation-ready
- **Nitrogen:** ON HOLD — methodology proven, data pipeline not yet started
- **Quantum:** Separate R&D track — 9 experiments, 0 positive lift, closed
- **Work packets:** 30 closed (P-001 through P-030), 14 Confirmed, 6 Negative, 4 Promising

## Links

- Website: [materiaarche.com](https://materiaarche.com)
- Evidence: [Google Drive](https://drive.google.com/drive/folders/1b2zZAfkEcxQH6TERfDJ-YCb1uvEo-TEz?usp=sharing)
