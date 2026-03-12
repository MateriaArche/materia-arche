# Phase 2 — Partner Outreach Template

**Version:** 1.0
**Date:** 2026-03-12

---

## Email template

**Subject:** Prospective blinded pilot for within-family perovskite stability ranking

Dear Dr. [Name],

We are running a frozen Phase 2 validation of a machine-learning model that ranks fabrication choices within a perovskite composition family by predicted stability.

This is **not** a cross-family or mechanism claim. The pilot is pre-registered, blinded, and uses a fixed test matrix of 45 devices across 3 composition families, with MPP tracking as the primary endpoint and mandatory fabrication metadata capture.

The model has been validated internally across 48 work packets on 1,543 devices from the Perovskite Database, with Kendall tau-b 0.27–0.34 for within-family ranking. Full evidence (66 notebooks, all code and data) is public at https://github.com/MateriaArche/materia-arche.

We are looking for a partner who can either fabricate the devices under a fixed stack, independently run the stability/metrology protocol, or both. I have attached:

1. **Scope and Non-Claims** — what the pilot validates and what it does not
2. **Test Matrix** — 45-device design, blinding protocol, pass/fail gates
3. **Metadata Template** — mandatory fields per device

Could you let us know whether this fits your capabilities, and if so, what an indicative budget range would be for:

(a) Fabrication only (45 devices, 9 recipes, fixed stack)
(b) Fabrication + indoor stability testing (MPP tracking, periodic JV)
(c) Fabrication + indoor stability testing + limited post-mortem on outliers (PL/EL/XRD)

We are also open to a two-partner structure where one group fabricates and a second group runs the blinded stability protocol independently.

Best regards,
[Name]
Materia Arche
https://materiaarche.com

---

## Screening questions for partner evaluation

Ask every candidate lab the same five questions:

1. Can you fabricate all recipes under one fixed stack (same substrate, architecture, encapsulation) while keeping only the intended recipe variables isolated?
2. Can you run **MPP tracking as the primary endpoint** and export raw time-series data (CSV, timestamped)?
3. Will you capture every field in our metadata template, with missing critical fields treated as protocol deviations?
4. Can you support blinded sample IDs and a frozen analysis plan (no unblinding until all data is collected and locked)?
5. What is your indicative budget for scopes (a), (b), and (c) above?

## Partner shortlist

Priority order for initial outreach:

| Priority | Lab | Role | Contact | Why |
|----------|-----|------|---------|-----|
| 1 | ICN2 Barcelona (Lira-Cantú group) | Fabrication | monica.lira@icn2.cat | Solution-processed perovskites, ISOS protocol expertise, degradation studies |
| 2 | CENER Navarra | Independent testing/metrology | business@cener.com | ENAC/IEC accredited PV lab, perovskite characterization since 2025 |
| 3 | ITER Tenerife (LabCelFV) | Budget fabrication backup | cmontes@iter.es | Deposition methods + atmospheric stability evaluation |
| 4 | UNIZAR Zaragoza (ParaSol/OSS) | Outdoor follow-on (Phase 2b) | ejjuarezperez@unizar.es | Continuous MPP outdoor monitoring platform |
| 5 | Fraunhofer ISE | High-credibility reserve | Via perovskite program page | Industrial-grade execution, higher budget |

## Recommended structure

**Preferred:** ICN2 fabricates + CENER tests (two-partner, highest credibility)
**Budget fallback:** ITER fabricates + tests (single-lab, lean)
**Follow-on:** Zaragoza outdoor subset after indoor pilot clears

## Attachments to send

- Phase2_Scope_and_Non_Claims.md (convert to PDF)
- Phase2_Test_Matrix.md (convert to PDF)
- Phase2_Metadata_Template.md (convert to PDF)

---

*Do not modify partner shortlist contacts without verifying they are current.*
