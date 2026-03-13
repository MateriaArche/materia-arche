# Phase 2 — Two-Stage Freeze Checklist

**Version:** 1.0
**Date:** 2026-03-13

---

## Freeze A: Scientific Lock (lab-agnostic — freeze NOW)

Lock these before serious outreach. They define what is being tested and how success is measured. None depend on which lab is chosen.

| Item | File | Status |
|------|------|--------|
| Model binary (31-feature ET) | `freeze_a/model.pkl` | TODO |
| Training data snapshot | `freeze_a/training_data.csv` | TODO |
| Feature list (ordered) | `freeze_a/features.json` | TODO |
| Feature engineering code | `freeze_a/feature_engineering.py` | TODO |
| Inference script | `freeze_a/predict.py` | TODO |
| Conformal calibration parameters | `freeze_a/conformal_params.json` | TODO |
| Selection logic (rank → recipe class) | `freeze_a/selection_logic.md` | TODO |
| Primary endpoint definition | `Phase2_Test_Matrix.md` §Primary endpoint | DONE |
| Pass/fail gates | `Phase2_Test_Matrix.md` §Pass/fail gates | DONE |
| Analysis script | `freeze_a/analysis.py` | TODO |
| Metadata schema + validator | `freeze_a/metadata_validator.py` | TODO |
| Blinding scheme | `freeze_a/blinding.md` | TODO |
| Protocol deviation rules | `freeze_a/deviations.md` | TODO |
| Scope and non-claims | `Phase2_Scope_and_Non_Claims.md` | DONE |
| Test matrix (structure only) | `Phase2_Test_Matrix.md` | DONE |
| Metadata template | `Phase2_Metadata_Template.md` | DONE |
| Negative result templates | `freeze_a/negative_templates.md` | TODO |
| Python environment | `freeze_a/requirements.txt` | TODO |
| SHA-256 manifest | `freeze_a/MANIFEST.sha256` | TODO |

**Freeze A trigger:** All items above marked DONE. Compute manifest hash. Tag git commit as `freeze-a-v1`. No modifications after tag without version bump and documented rationale.

---

## Freeze B: Execution Lock (lab-specific — freeze AFTER partner selection)

These depend on what the partner can actually fabricate. Freezing them early risks validating "recipe transfer failure" instead of the model.

| Item | Depends on | Status |
|------|-----------|--------|
| Exact recipe instantiations per family | Lab's process envelope | WAIT |
| Exact stack details (substrate, architecture, contacts) | Lab's standard stack | WAIT |
| Solvent availability and purity specs | Lab's supply chain | WAIT |
| Annealing windows (equipment-constrained) | Lab's furnace/hotplate specs | WAIT |
| Encapsulation material and method | Lab's capability | WAIT |
| Chamber settings and MPP tracking cadence | Lab's equipment | WAIT |
| Post-mortem menu (which diagnostics, on how many) | Lab's characterization suite | WAIT |
| Materials procurement (who buys what) | Budget agreement | WAIT |
| Shipping/handoff/storage logistics | Two-partner vs single-lab | WAIT |
| Final sample map (device IDs → recipes) | Blinding + fabrication order | WAIT |
| Execution calendar | Lab availability | WAIT |
| Named personnel | Lab staffing | WAIT |
| Lab-specific SOP appendix | Lab's internal procedures | WAIT |
| QA/QC chain of custody | Lab + testing partner | WAIT |
| Safety/compliance paperwork | Institutional requirements | WAIT |
| Final budget and PO | Quotes received | WAIT |

**Freeze B trigger:** Partner selected, budget agreed, recipes validated against lab's process envelope. Tag git commit as `freeze-b-v1`.

---

## Critical rule

> If partner capability forces stack changes between families, the study becomes a **feasibility pilot**, not a **decisive validation**. Document this explicitly if it occurs.

---

## Version control

| Event | Action |
|-------|--------|
| Freeze A locked | Git tag `freeze-a-v1`, manifest computed |
| Any Freeze A change | Version bump (`freeze-a-v2`), documented rationale required |
| Partner selected | Begin Freeze B items |
| Freeze B locked | Git tag `freeze-b-v1`, full manifest updated |
| Any Freeze B change | Version bump, documented rationale, check if Freeze A affected |
| Pilot launch | Both freezes locked, no changes until all data collected |
