# Phase 2 — Mandatory Metadata Capture Template

**Version:** 1.0
**Date:** 2026-03-12

---

## Purpose

Every device fabricated in the Phase 2 pilot must have complete metadata for the fields below. Missing key metadata counts as a **protocol deviation** and may exclude the device from analysis.

This is not paperwork. P-046 showed that fabrication process variables (solvents, layer thicknesses, annealing conditions) are the model's most important features. Incomplete metadata makes the pilot data useless for future model improvement.

---

## Required fields per device

### Identity
| Field | Description | Example |
|-------|-------------|---------|
| Device_ID | Unique blinded identifier | P2-MA-007 |
| Batch_ID | Fabrication batch | B-2026-03-A |
| Family | Composition family | Pure MA |
| Recipe_class | Model-favored / Baseline / Negative control | Model-favored |
| Operator_ID | Person who fabricated | Op-1 |
| Fabrication_date | ISO 8601 | 2026-04-15 |

### Composition
| Field | Description | Units |
|-------|-------------|-------|
| Perovskite_composition | Full stoichiometry | MAPbI₃ |
| MA_fraction | Methylammonium fraction | 0–1 |
| FA_fraction | Formamidinium fraction | 0–1 |
| Cs_fraction | Cesium fraction | 0–1 |
| Pb_fraction | Lead fraction | 0–1 |
| Sn_fraction | Tin fraction | 0–1 |
| I_fraction | Iodide fraction | 0–3 |
| Br_fraction | Bromide fraction | 0–3 |
| Cl_fraction | Chloride fraction | 0–3 |

### Solvents (CRITICAL — top feature group from P-046)
| Field | Description | Units |
|-------|-------------|-------|
| DMF_volume | DMF volume fraction | 0–1 |
| DMSO_volume | DMSO volume fraction | 0–1 |
| Other_solvent | Other solvent name + fraction | text + 0–1 |
| DMF_DMSO_ratio | DMF:DMSO ratio | numeric |
| Antisolvent | Antisolvent used | text |
| Antisolvent_volume | Volume used | µL |
| Antisolvent_drip_time | Time after spin start | s |

### Deposition
| Field | Description | Units |
|-------|-------------|-------|
| Deposition_method | Spin-coat / blade / evaporation | text |
| Spin_speed | RPM for each step | RPM |
| Spin_duration | Duration for each step | s |
| Deposition_atmosphere | N₂ / air / glovebox | text |
| Deposition_RH | Relative humidity during deposition | % |
| Deposition_temperature | Substrate temperature | °C |

### Annealing (CRITICAL — top feature from P-033)
| Field | Description | Units |
|-------|-------------|-------|
| Anneal_temperature | Primary annealing temperature | °C |
| Anneal_time | Primary annealing duration | min |
| Anneal_atmosphere | N₂ / air / vacuum | text |
| Anneal_RH | Relative humidity during annealing | % |
| Total_thermal_exposure | Temperature × time integral | °C·min |

### Layer thicknesses (CRITICAL — second feature group from P-046)
| Field | Description | Units |
|-------|-------------|-------|
| Perovskite_thickness | Perovskite layer | nm |
| ETL_material | Electron transport layer material | text |
| ETL_thickness | ETL thickness | nm |
| HTL_material | Hole transport layer material | text |
| HTL_thickness | HTL thickness | nm |
| Backcontact_material | Back contact material | text |
| Backcontact_thickness | Back contact thickness | nm |

### Device geometry
| Field | Description | Units |
|-------|-------------|-------|
| Cell_area | Active area measured | cm² |
| Substrate | Glass / flexible / other | text |
| Stack_sequence | Full layer sequence | text |
| Encapsulation | Material and method | text |

### JV characterization (pre-ageing)
| Field | Description | Units |
|-------|-------------|-------|
| Voc | Open-circuit voltage | V |
| Jsc | Short-circuit current density | mA/cm² |
| FF | Fill factor | 0–1 |
| PCE | Power conversion efficiency | % |
| JV_scan_direction | Forward / reverse / both | text |
| JV_scan_rate | Scan speed | mV/s |
| JV_light_source | Solar simulator type | text |

### Ageing protocol
| Field | Description | Units |
|-------|-------------|-------|
| Ageing_protocol | ISOS category (e.g., ISOS-L-1) | text |
| Light_source | Type and spectrum | text |
| Light_intensity | Irradiance | mW/cm² |
| Ageing_temperature | Temperature during ageing | °C |
| Ageing_RH | Relative humidity during ageing | % |
| Bias_condition | MPP / open-circuit / short-circuit | text |
| Measurement_cadence | How often MPP/JV recorded | hours |
| Preconditioning | Light soak / dark storage before test | text |

### Ageing results
| Field | Description | Units |
|-------|-------------|-------|
| MPP_timeseries | Full MPP tracking data file path | file |
| T80 | Time to 80% of initial PCE | hours |
| T95 | Time to 95% of initial PCE | hours |
| Degradation_curve_shape | Linear / exponential / burn-in+stable / other | text |
| JV_periodic | Periodic JV snapshots file path | file |

### Post-mortem (required for outliers — top/bottom 20% performers)
| Field | Description | Units |
|-------|-------------|-------|
| PL_imaging | Photoluminescence image file | file |
| EL_imaging | Electroluminescence image file | file |
| XRD_scan | X-ray diffraction data file | file |
| Failure_mode_hypothesis | Operator assessment of likely failure mode | text |
| Additional_characterization | Any additional analysis performed | text |

---

## Data format

- All time-series data: CSV with columns `timestamp_hours, value`
- All metadata: one row per device in a master spreadsheet
- File naming: `{Device_ID}_{measurement_type}.csv`
- All files stored in a single shared directory per batch

## Protocol deviations

Any missing **CRITICAL** field (solvents, annealing, layer thicknesses, cell area) must be documented as a protocol deviation with explanation. Devices with >3 missing critical fields are excluded from primary analysis.

---

*This template is part of the frozen artifact set for Phase 2.*
