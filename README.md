**Important:** Please read [Honesty Note](README_Honesty_Note.md) first.

# Materia Arche

ML-orchestrated stability prediction for perovskite solar cells.

## What this is

An end-to-end pipeline that ranks perovskite compositions by predicted T80 stability, validated against 1,543 devices from the Perovskite Database Project.

- **Best model:** ExtraTreesRegressor — Kendall tau-b 0.271 (CV 0.289)
- **Classical baseline lift:** +0.155 over composition-only ranking
- **SHAP top drivers:** Jsc, bandgap, Voc
- **Quantum experiments:** 9 tested, 0 positive lift (closed as research track)
- **Lab panel:** 3 candidates selected for Phase 2 external validation

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

## Current status

- **Perovskite:** Phase 2 ACTIVE — production model locked, lab panel selected
- **Nitrogen:** ON HOLD — methodology proven, data pipeline not yet started
- **Quantum:** Separate R&D track — not a gate

## Links

- Website: [materiaarche.com](https://materiaarche.com)
- Evidence: [Google Drive](https://drive.google.com/drive/folders/1b2zZAfkEcxQH6TERfDJ-YCb1uvEo-TEz?usp=sharing)
