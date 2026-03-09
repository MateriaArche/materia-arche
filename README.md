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
- **Lab panel:** 3 diversified candidates locked via P-005→P-007, E4 validation-ready
- **Work packets:** 8 closed (P-001 through P-008), 3 Confirmed

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

## Current status

- **Perovskite:** Phase 2 ACTIVE — production model locked, diversified lab panel confirmed (P-007)
- **Lab panel:** 3 compositions across 3 families, all 100% top-20 rate — E4 validation-ready
- **Nitrogen:** ON HOLD — methodology proven, data pipeline not yet started
- **Quantum:** Separate R&D track — 9 experiments, 0 positive lift, closed
- **Work packets:** 8 closed (P-001 through P-008), 3 Confirmed

## Links

- Website: [materiaarche.com](https://materiaarche.com)
- Evidence: [Google Drive](https://drive.google.com/drive/folders/1b2zZAfkEcxQH6TERfDJ-YCb1uvEo-TEz?usp=sharing)
