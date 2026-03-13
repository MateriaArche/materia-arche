"""
Metadata validator for Phase 2 pilot.

Validates incoming lab data against the mandatory metadata schema.
Flags missing critical fields as protocol deviations.
Do not modify after Freeze A is locked.
"""
import pandas as pd
import sys
import os

# Critical fields — missing any of these is a protocol deviation
CRITICAL_FIELDS = [
    'Device_ID',
    'Family',
    'Recipe_class',
    'Perovskite_composition',
    # Solvents (top feature group from P-046)
    'DMF_volume',
    'DMSO_volume',
    'DMF_DMSO_ratio',
    # Annealing (top feature from P-033)
    'Anneal_temperature',
    'Anneal_time',
    # Layer thicknesses (second feature group from P-046)
    'Perovskite_thickness',
    'ETL_thickness',
    'Backcontact_thickness',
    # Device geometry
    'Cell_area',
    # JV pre-ageing
    'Voc',
    'Jsc',
    'FF',
    'PCE',
    # Ageing
    'Ageing_protocol',
    'T80',
]

# Required but non-critical fields
REQUIRED_FIELDS = [
    'Batch_ID',
    'Operator_ID',
    'Fabrication_date',
    'MA_fraction',
    'FA_fraction',
    'Cs_fraction',
    'Pb_fraction',
    'I_fraction',
    'Br_fraction',
    'Deposition_method',
    'Deposition_atmosphere',
    'Anneal_atmosphere',
    'HTL_thickness',
    'ETL_material',
    'HTL_material',
    'Backcontact_material',
    'Stack_sequence',
    'Encapsulation',
    'Light_source',
    'Light_intensity',
    'Ageing_temperature',
    'Ageing_RH',
    'Bias_condition',
    'Measurement_cadence',
    'MPP_timeseries',
]

# Fields that should be numeric
NUMERIC_FIELDS = [
    'DMF_volume', 'DMSO_volume', 'DMF_DMSO_ratio',
    'Anneal_temperature', 'Anneal_time',
    'Perovskite_thickness', 'ETL_thickness', 'HTL_thickness', 'Backcontact_thickness',
    'Cell_area', 'Voc', 'Jsc', 'FF', 'PCE', 'T80',
    'MA_fraction', 'FA_fraction', 'Cs_fraction', 'Pb_fraction',
    'I_fraction', 'Br_fraction',
    'Light_intensity', 'Ageing_temperature', 'Ageing_RH',
]

# Valid values for categorical fields
VALID_CATEGORIES = {
    'Recipe_class': ['model-favored', 'baseline', 'negative-control'],
    'Family': ['Pure MA', 'Pure FA', 'MA-FA mixed', 'FA-Cs', 'Triple cation', 'Other'],
    'Deposition_method': ['spin-coat', 'blade', 'evaporation', 'slot-die', 'other'],
    'Bias_condition': ['MPP', 'open-circuit', 'short-circuit', 'other'],
}


def validate_metadata(csv_path):
    """
    Validate a metadata CSV file.

    Returns a report dict with:
        - valid: bool
        - n_devices: int
        - critical_missing: list of (device, field) tuples
        - required_missing: list of (device, field) tuples
        - type_errors: list of (device, field, value) tuples
        - category_errors: list of (device, field, value) tuples
        - deviations: int (count of critical missing)
        - completeness: float (fraction of all fields present)
    """
    df = pd.read_csv(csv_path)

    report = {
        'valid': True,
        'n_devices': len(df),
        'critical_missing': [],
        'required_missing': [],
        'type_errors': [],
        'category_errors': [],
        'deviations': 0,
        'completeness': 0.0,
    }

    all_fields = CRITICAL_FIELDS + REQUIRED_FIELDS
    total_cells = len(df) * len(all_fields)
    filled_cells = 0

    for _, row in df.iterrows():
        device_id = row.get('Device_ID', f'row_{_}')

        # Check critical fields
        for field in CRITICAL_FIELDS:
            if field not in df.columns or pd.isna(row.get(field)):
                report['critical_missing'].append((device_id, field))
                report['deviations'] += 1
                report['valid'] = False
            else:
                filled_cells += 1

        # Check required fields
        for field in REQUIRED_FIELDS:
            if field not in df.columns or pd.isna(row.get(field)):
                report['required_missing'].append((device_id, field))
            else:
                filled_cells += 1

        # Check numeric types
        for field in NUMERIC_FIELDS:
            if field in df.columns and not pd.isna(row.get(field)):
                try:
                    float(row[field])
                except (ValueError, TypeError):
                    report['type_errors'].append((device_id, field, row[field]))

        # Check categorical values
        for field, valid_vals in VALID_CATEGORIES.items():
            if field in df.columns and not pd.isna(row.get(field)):
                if str(row[field]).lower() not in [v.lower() for v in valid_vals]:
                    report['category_errors'].append((device_id, field, row[field]))

    report['completeness'] = filled_cells / total_cells if total_cells > 0 else 0

    return report


def print_report(report):
    """Print a human-readable validation report."""
    print(f"\n{'=' * 60}")
    print(f"METADATA VALIDATION REPORT")
    print(f"{'=' * 60}")
    print(f"Devices:      {report['n_devices']}")
    print(f"Valid:         {'YES' if report['valid'] else 'NO'}")
    print(f"Completeness: {report['completeness']:.1%}")
    print(f"Deviations:   {report['deviations']}")

    if report['critical_missing']:
        print(f"\n--- CRITICAL MISSING ({len(report['critical_missing'])}) ---")
        print("Each is a PROTOCOL DEVIATION:")
        for device, field in report['critical_missing'][:20]:
            print(f"  {device}: missing {field}")
        if len(report['critical_missing']) > 20:
            print(f"  ... and {len(report['critical_missing']) - 20} more")

    if report['required_missing']:
        print(f"\n--- Required missing ({len(report['required_missing'])}) ---")
        for device, field in report['required_missing'][:20]:
            print(f"  {device}: missing {field}")
        if len(report['required_missing']) > 20:
            print(f"  ... and {len(report['required_missing']) - 20} more")

    if report['type_errors']:
        print(f"\n--- Type errors ({len(report['type_errors'])}) ---")
        for device, field, value in report['type_errors'][:10]:
            print(f"  {device}: {field} = '{value}' (expected numeric)")

    if report['category_errors']:
        print(f"\n--- Category errors ({len(report['category_errors'])}) ---")
        for device, field, value in report['category_errors'][:10]:
            valid = VALID_CATEGORIES.get(field, [])
            print(f"  {device}: {field} = '{value}' (expected one of {valid})")

    # Exclusion check
    devices_with_3plus_critical = {}
    for device, field in report['critical_missing']:
        devices_with_3plus_critical[device] = devices_with_3plus_critical.get(device, 0) + 1

    excluded = [d for d, n in devices_with_3plus_critical.items() if n > 3]
    if excluded:
        print(f"\n--- EXCLUDED DEVICES ({len(excluded)}) ---")
        print("Devices with >3 missing critical fields (excluded from primary analysis):")
        for d in excluded:
            print(f"  {d} ({devices_with_3plus_critical[d]} missing critical fields)")

    print(f"\n{'=' * 60}")
    if report['valid']:
        print("RESULT: PASS — all critical fields present")
    else:
        print(f"RESULT: FAIL — {report['deviations']} protocol deviations")
    print(f"{'=' * 60}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python metadata_validator.py <metadata.csv>")
        print("\nGenerating sample template...")

        # Generate empty template CSV
        all_fields = CRITICAL_FIELDS + [f for f in REQUIRED_FIELDS if f not in CRITICAL_FIELDS]
        template = pd.DataFrame(columns=all_fields)
        template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      '..', 'Phase2_Metadata_Template.csv')
        template.to_csv(template_path, index=False)
        print(f"Saved empty template to: {template_path}")
    else:
        report = validate_metadata(sys.argv[1])
        print_report(report)
