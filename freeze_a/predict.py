"""
Frozen inference script for Phase 2.

Loads the frozen model and generates rankings with conformal intervals.
Do not modify after Freeze A is locked.
"""
import pandas as pd
import numpy as np
import json
import pickle
import os
import sys

FREEZE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_frozen_model():
    """Load the frozen model and configuration."""
    with open(os.path.join(FREEZE_DIR, 'model.pkl'), 'rb') as f:
        model = pickle.load(f)

    with open(os.path.join(FREEZE_DIR, 'features.json'), 'r') as f:
        config = json.load(f)

    with open(os.path.join(FREEZE_DIR, 'conformal_params.json'), 'r') as f:
        conformal = json.load(f)

    return model, config, conformal


def classify_family(row):
    """Assign composition family from A-site cation fractions."""
    ma = (row.get('MA', 0) or 0) > 0
    fa = (row.get('FA', 0) or 0) > 0
    cs = (row.get('Cs', 0) or 0) > 0
    if ma and not fa and not cs:
        return "Pure MA"
    elif fa and not ma and not cs:
        return "Pure FA"
    elif ma and fa and not cs:
        return "MA-FA mixed"
    elif fa and cs and not ma:
        return "FA-Cs"
    elif ma and fa and cs:
        return "Triple cation"
    else:
        return "Other"


def predict_and_rank(df, family=None):
    """
    Generate rankings with conformal intervals.

    Parameters
    ----------
    df : DataFrame
        Must contain all 31 features (missing values will be filled with 0).
    family : str, optional
        If provided, rank only within this family.

    Returns
    -------
    DataFrame with columns:
        - predicted_log1p_T80: raw model prediction
        - predicted_T80_hours: expm1 of prediction
        - ci_lower, ci_upper: conformal interval bounds (in hours)
        - family: composition family
        - within_family_rank: rank within family (1 = best)
        - global_rank: rank across all devices (1 = best)
    """
    model, config, conformal = load_frozen_model()

    features = config['features']
    q_hat = conformal['q_hat']

    X = df[features].fillna(config['fillna_value'])
    preds = model.predict(X)

    # Conformal intervals (in log1p space, then transform)
    ci_lower_log = preds - q_hat
    ci_upper_log = preds + q_hat

    results = df.copy()
    results['predicted_log1p_T80'] = preds
    results['predicted_T80_hours'] = np.expm1(preds)
    results['ci_lower_hours'] = np.expm1(ci_lower_log)
    results['ci_upper_hours'] = np.expm1(ci_upper_log)
    results['family'] = df.apply(classify_family, axis=1)

    # Global ranking (1 = highest predicted stability)
    results['global_rank'] = results['predicted_log1p_T80'].rank(
        ascending=False, method='min'
    ).astype(int)

    # Within-family ranking
    results['within_family_rank'] = results.groupby('family')[
        'predicted_log1p_T80'
    ].rank(ascending=False, method='min').astype(int)

    if family:
        results = results[results['family'] == family].copy()

    return results.sort_values('global_rank')


def select_recipes(df, family, n_top=3, n_bottom=3):
    """
    Select model-favored and negative-control recipes for a family.

    Returns top-N and bottom-N ranked devices within the specified family.
    """
    ranked = predict_and_rank(df, family=family)
    n_family = len(ranked)

    top = ranked.head(n_top).copy()
    top['recipe_class'] = 'model-favored'

    bottom = ranked.tail(n_bottom).copy()
    bottom['recipe_class'] = 'negative-control'

    print(f"\n{'=' * 60}")
    print(f"RECIPE SELECTION — {family} (n={n_family})")
    print(f"{'=' * 60}")
    print(f"\nModel-favored (top {n_top}):")
    for _, row in top.iterrows():
        print(f"  Rank {int(row['within_family_rank']):>4}: "
              f"predicted T80 = {row['predicted_T80_hours']:.0f}h "
              f"[{row['ci_lower_hours']:.0f}, {row['ci_upper_hours']:.0f}]")

    print(f"\nNegative control (bottom {n_bottom}):")
    for _, row in bottom.iterrows():
        print(f"  Rank {int(row['within_family_rank']):>4}: "
              f"predicted T80 = {row['predicted_T80_hours']:.0f}h "
              f"[{row['ci_lower_hours']:.0f}, {row['ci_upper_hours']:.0f}]")

    return pd.concat([top, bottom])


if __name__ == '__main__':
    # Demo: rank the training data
    data_path = os.path.join(FREEZE_DIR, 'training_data.csv')
    df = pd.read_csv(data_path)

    print("Frozen model inference demo")
    print(f"Loaded {len(df)} devices")

    ranked = predict_and_rank(df)
    print(f"\nTop 10 globally:")
    for _, row in ranked.head(10).iterrows():
        print(f"  Global #{int(row['global_rank']):>4} | {row['family']:<15} | "
              f"T80 = {row['predicted_T80_hours']:.0f}h "
              f"[{row['ci_lower_hours']:.0f}, {row['ci_upper_hours']:.0f}]")

    # Select recipes for each panel family
    for family in ['Pure MA', 'MA-FA mixed', 'FA-Cs']:
        select_recipes(df, family)
