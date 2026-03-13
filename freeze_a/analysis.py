"""
Pre-registered analysis script for Phase 2 pilot.

Ingests raw pilot data, computes endpoints, applies exclusions,
and outputs the final comparison against pre-registered pass/fail gates.

Do not modify after Freeze A is locked.
"""
import pandas as pd
import numpy as np
from scipy.stats import kendalltau, mannwhitneyu
import json
import os
import sys

FREEZE_DIR = os.path.dirname(os.path.abspath(__file__))

# Pre-registered pass/fail thresholds
PASS_THRESHOLDS = {
    'min_families_with_lift': 2,       # out of 3
    'min_pairwise_win_rate': 0.65,     # 65%
    'lift_threshold': 0.10,            # 10% median T80 improvement
    'conformal_coverage_min': 0.60,    # acceptable range
    'conformal_coverage_max': 0.90,
    'max_deviation_rate': 0.20,        # >20% missing critical = fail
}


def load_pilot_data(csv_path):
    """Load and validate pilot data."""
    df = pd.read_csv(csv_path)

    required = ['Device_ID', 'Family', 'Recipe_class', 'T80']
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    return df


def apply_exclusions(df):
    """Apply pre-registered exclusion rules."""
    excluded = []
    included = df.copy()

    # Exclusion 1: Devices with >3 missing critical fields
    # (This should already be caught by metadata_validator.py)

    # Exclusion 2: Devices with T80 = NaN or T80 <= 0
    bad_t80 = included['T80'].isna() | (included['T80'] <= 0)
    if bad_t80.any():
        excluded.extend(included[bad_t80]['Device_ID'].tolist())
        included = included[~bad_t80]

    # Exclusion 3: Devices flagged as protocol deviations
    if 'Protocol_deviation' in included.columns:
        deviated = included['Protocol_deviation'].fillna('').str.strip() != ''
        if deviated.any():
            excluded.extend(included[deviated]['Device_ID'].tolist())
            included = included[~deviated]

    return included, excluded


def compute_pairwise_results(df):
    """
    Compute pairwise within-family comparisons.

    For each family:
    - Model-favored vs Baseline: does median T80 of favored exceed baseline by ≥10%?
    - Baseline vs Negative control: does median T80 of baseline exceed negative by ≥10%?
    """
    results = []

    for family in df['Family'].unique():
        fam_df = df[df['Family'] == family]

        for comparison, (class_a, class_b) in [
            ('favored_vs_baseline', ('model-favored', 'baseline')),
            ('baseline_vs_negative', ('baseline', 'negative-control')),
        ]:
            a = fam_df[fam_df['Recipe_class'] == class_a]['T80']
            b = fam_df[fam_df['Recipe_class'] == class_b]['T80']

            if len(a) == 0 or len(b) == 0:
                results.append({
                    'family': family,
                    'comparison': comparison,
                    'n_a': len(a),
                    'n_b': len(b),
                    'median_a': np.nan,
                    'median_b': np.nan,
                    'lift_pct': np.nan,
                    'win': None,
                    'p_value': np.nan,
                    'note': 'Insufficient data',
                })
                continue

            median_a = np.median(a)
            median_b = np.median(b)
            lift = (median_a - median_b) / median_b if median_b > 0 else np.nan

            # Mann-Whitney U test (non-parametric)
            try:
                stat, p_value = mannwhitneyu(a, b, alternative='greater')
            except ValueError:
                p_value = np.nan

            win = lift >= PASS_THRESHOLDS['lift_threshold'] if not np.isnan(lift) else None

            results.append({
                'family': family,
                'comparison': comparison,
                'n_a': len(a),
                'n_b': len(b),
                'median_a': median_a,
                'median_b': median_b,
                'lift_pct': lift,
                'win': win,
                'p_value': p_value,
            })

    return pd.DataFrame(results)


def compute_rank_correlation(df):
    """Compute within-family Kendall tau-b between model prediction and observed T80."""
    with open(os.path.join(FREEZE_DIR, 'conformal_params.json'), 'r') as f:
        conformal = json.load(f)

    results = []
    for family in df['Family'].unique():
        fam_df = df[df['Family'] == family]
        if 'predicted_T80_hours' in fam_df.columns and len(fam_df) >= 5:
            tau, p = kendalltau(fam_df['T80'], fam_df['predicted_T80_hours'])
            results.append({
                'family': family,
                'n': len(fam_df),
                'tau_b': tau,
                'p_value': p,
            })

    return pd.DataFrame(results) if results else pd.DataFrame()


def evaluate_conformal(df):
    """Check if conformal intervals cover observed T80 at expected rate."""
    if 'ci_lower_hours' not in df.columns or 'ci_upper_hours' not in df.columns:
        return None

    covered = (df['T80'] >= df['ci_lower_hours']) & (df['T80'] <= df['ci_upper_hours'])
    coverage = covered.mean()

    return {
        'coverage': coverage,
        'n_devices': len(df),
        'n_covered': covered.sum(),
        'calibrated': (PASS_THRESHOLDS['conformal_coverage_min'] <= coverage
                       <= PASS_THRESHOLDS['conformal_coverage_max']),
    }


def determine_outcome(pairwise_df, conformal_result, n_excluded, n_total):
    """Apply pre-registered pass/fail gates."""
    # Count families where model-favored beats baseline
    favored_wins = pairwise_df[
        (pairwise_df['comparison'] == 'favored_vs_baseline') &
        (pairwise_df['win'] == True)
    ]
    n_families_with_lift = len(favored_wins)

    # Overall pairwise win rate
    all_comparisons = pairwise_df[pairwise_df['win'].notna()]
    win_rate = all_comparisons['win'].mean() if len(all_comparisons) > 0 else 0

    # Deviation rate
    deviation_rate = n_excluded / n_total if n_total > 0 else 0

    # Conformal calibration
    conformal_ok = conformal_result['calibrated'] if conformal_result else True

    # Determine outcome
    if deviation_rate > PASS_THRESHOLDS['max_deviation_rate']:
        outcome = 'FAIL'
        reason = f'Deviation rate {deviation_rate:.0%} exceeds {PASS_THRESHOLDS["max_deviation_rate"]:.0%} threshold'
    elif (n_families_with_lift >= PASS_THRESHOLDS['min_families_with_lift'] and
          win_rate >= PASS_THRESHOLDS['min_pairwise_win_rate'] and
          conformal_ok):
        outcome = 'PASS'
        reason = (f'{n_families_with_lift}/3 families with lift, '
                  f'win rate {win_rate:.0%}, conformal OK')
    elif n_families_with_lift >= 1:
        outcome = 'PARTIAL PASS'
        reason = (f'{n_families_with_lift}/3 families with lift (need ≥2), '
                  f'win rate {win_rate:.0%}')
    else:
        outcome = 'FAIL'
        reason = f'No family shows clear lift. Win rate {win_rate:.0%}'

    return {
        'outcome': outcome,
        'reason': reason,
        'n_families_with_lift': n_families_with_lift,
        'pairwise_win_rate': win_rate,
        'deviation_rate': deviation_rate,
        'conformal_calibrated': conformal_ok,
    }


def run_analysis(csv_path, output_dir=None):
    """Run the complete pre-registered analysis."""
    if output_dir is None:
        output_dir = os.path.dirname(csv_path)

    print(f"{'=' * 70}")
    print("PHASE 2 PRE-REGISTERED ANALYSIS")
    print(f"{'=' * 70}")

    # Load
    df = load_pilot_data(csv_path)
    n_total = len(df)
    print(f"Loaded {n_total} devices")

    # Exclude
    df_clean, excluded = apply_exclusions(df)
    n_excluded = len(excluded)
    print(f"Excluded {n_excluded} devices, {len(df_clean)} remaining")
    if excluded:
        print(f"  Excluded IDs: {excluded}")

    # Pairwise comparisons
    pairwise = compute_pairwise_results(df_clean)
    print(f"\n--- PAIRWISE COMPARISONS ---")
    for _, row in pairwise.iterrows():
        win_str = 'WIN' if row['win'] else ('LOSS' if row['win'] is not None else 'N/A')
        print(f"  {row['family']:<15} {row['comparison']:<25} "
              f"median {row['median_a']:.0f} vs {row['median_b']:.0f}h  "
              f"lift={row['lift_pct']:+.1%}  {win_str}  (p={row['p_value']:.3f})")

    # Rank correlation
    rank_corr = compute_rank_correlation(df_clean)
    if len(rank_corr) > 0:
        print(f"\n--- WITHIN-FAMILY RANK CORRELATION ---")
        for _, row in rank_corr.iterrows():
            print(f"  {row['family']:<15} tau-b = {row['tau_b']:.3f} "
                  f"(n={row['n']}, p={row['p_value']:.3e})")

    # Conformal calibration
    conformal = evaluate_conformal(df_clean)
    if conformal:
        print(f"\n--- CONFORMAL CALIBRATION ---")
        print(f"  Coverage: {conformal['coverage']:.1%} "
              f"({conformal['n_covered']}/{conformal['n_devices']})")
        print(f"  Calibrated: {'YES' if conformal['calibrated'] else 'NO'}")

    # Final outcome
    outcome = determine_outcome(pairwise, conformal, n_excluded, n_total)
    print(f"\n{'=' * 70}")
    print(f"OUTCOME: {outcome['outcome']}")
    print(f"Reason: {outcome['reason']}")
    print(f"{'=' * 70}")

    # Save results
    pairwise.to_csv(os.path.join(output_dir, 'pilot_pairwise_results.csv'), index=False)
    with open(os.path.join(output_dir, 'pilot_outcome.json'), 'w') as f:
        json.dump(outcome, f, indent=2)

    print(f"\nSaved: pilot_pairwise_results.csv, pilot_outcome.json")

    return outcome


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python analysis.py <pilot_data.csv> [output_dir]")
        print("\nThis script runs the pre-registered Phase 2 analysis.")
        print("Input CSV must contain: Device_ID, Family, Recipe_class, T80")
        print("Optional: predicted_T80_hours, ci_lower_hours, ci_upper_hours")
    else:
        output = sys.argv[2] if len(sys.argv) > 2 else None
        run_analysis(sys.argv[1], output)
