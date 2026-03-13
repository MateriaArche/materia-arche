"""
Build Freeze A artifact bundle.

Trains the 31-feature kitchen sink model on the full dataset,
saves all artifacts, and computes SHA-256 manifest.

Run once. Do not modify artifacts after manifest is computed.
"""
import pandas as pd
import numpy as np
import json
import hashlib
import os
import pickle
from sklearn.ensemble import ExtraTreesRegressor

FREEZE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(os.path.dirname(FREEZE_DIR), 'perovskite_stability_clean.csv')

# === Feature definitions ===
ORIGINAL_16 = [
    'Perovskite_band_gap', 'Pb', 'Sn', 'I', 'Br', 'Cl',
    'MA', 'FA', 'Cs',
    'first_Prvskt_annealing_temperature', 'first_Prvskt_thermal_annealing_time',
    'Perovskite_thickness', 'Cell_area_measured',
    'JV_default_Voc', 'JV_default_Jsc', 'JV_default_FF'
]

KITCHEN_SINK_EXTRA = [
    'DMF', 'DMSO', 'other_solvent', 'DMF_DMSO_ratio',
    'LLE_1', 'LLE_2', 'LLE_3', 'LLE_4',
    'Perovskite_annealing_thermal_exposure',
    'Backcontact_thickness_list', 'ETL_thickness', 'HTL_thickness_list',
    'others_A', 'others_B', 'others_X'
]

FEATURES = ORIGINAL_16 + KITCHEN_SINK_EXTRA
TARGET = 'Stability_PCE_T80'

ET_PARAMS = {
    'n_estimators': 700,
    'max_features': 'sqrt',
    'min_samples_split': 3,
    'min_samples_leaf': 1,
    'bootstrap': False,
    'random_state': 42,
}

# === Load and prepare data ===
print("Loading data...")
df = pd.read_csv(DATA_PATH)
X = df[FEATURES].fillna(0)
y = np.log1p(df[TARGET])

print(f"Training data: {len(df)} devices, {len(FEATURES)} features")

# === Train model ===
print("Training model...")
model = ExtraTreesRegressor(**ET_PARAMS)
model.fit(X, y)

# === Compute conformal calibration parameters ===
# Using split conformal: train on 80%, calibrate on 20%
from sklearn.model_selection import train_test_split

X_train, X_cal, y_train, y_cal = train_test_split(
    X, y, test_size=0.2, random_state=42
)
cal_model = ExtraTreesRegressor(**ET_PARAMS)
cal_model.fit(X_train, y_train)
cal_preds = cal_model.predict(X_cal)
cal_residuals = np.abs(y_cal.values - cal_preds)

# q-hat for 80% coverage
alpha = 0.20
q_hat = np.quantile(cal_residuals, 1 - alpha)

conformal_params = {
    'alpha': alpha,
    'q_hat': float(q_hat),
    'n_calibration': len(X_cal),
    'calibration_seed': 42,
    'nominal_coverage': 1 - alpha,
}

# === Save artifacts ===
print("Saving artifacts...")

# 1. Model binary
model_path = os.path.join(FREEZE_DIR, 'model.pkl')
with open(model_path, 'wb') as f:
    pickle.dump(model, f)

# 2. Training data snapshot
data_path = os.path.join(FREEZE_DIR, 'training_data.csv')
df.to_csv(data_path, index=False)

# 3. Feature list
features_path = os.path.join(FREEZE_DIR, 'features.json')
with open(features_path, 'w') as f:
    json.dump({
        'features': FEATURES,
        'target': TARGET,
        'target_transform': 'log1p',
        'fillna_value': 0,
        'n_features': len(FEATURES),
    }, f, indent=2)

# 4. Model parameters
params_path = os.path.join(FREEZE_DIR, 'model_params.json')
with open(params_path, 'w') as f:
    json.dump(ET_PARAMS, f, indent=2)

# 5. Conformal parameters
conformal_path = os.path.join(FREEZE_DIR, 'conformal_params.json')
with open(conformal_path, 'w') as f:
    json.dump(conformal_params, f, indent=2)

# 6. Requirements
reqs_path = os.path.join(FREEZE_DIR, 'requirements.txt')
with open(reqs_path, 'w') as f:
    f.write("pandas>=1.3\n")
    f.write("numpy>=1.21\n")
    f.write("scikit-learn>=1.0\n")
    f.write("scipy>=1.7\n")

# === Compute SHA-256 manifest ===
print("Computing manifest...")

manifest_files = [
    'model.pkl',
    'training_data.csv',
    'features.json',
    'model_params.json',
    'conformal_params.json',
    'requirements.txt',
    'build_freeze_a.py',
    'predict.py',
    'analysis.py',
    'metadata_validator.py',
]

manifest_path = os.path.join(FREEZE_DIR, 'MANIFEST.sha256')
with open(manifest_path, 'w') as mf:
    mf.write("# Freeze A SHA-256 Manifest\n")
    mf.write(f"# Generated: {pd.Timestamp.now().isoformat()}\n")
    mf.write(f"# Training samples: {len(df)}\n")
    mf.write(f"# Features: {len(FEATURES)}\n\n")

    for fname in manifest_files:
        fpath = os.path.join(FREEZE_DIR, fname)
        if os.path.exists(fpath):
            with open(fpath, 'rb') as f:
                h = hashlib.sha256(f.read()).hexdigest()
            mf.write(f"{h}  {fname}\n")
            print(f"  {fname}: {h[:16]}...")
        else:
            mf.write(f"MISSING  {fname}\n")
            print(f"  {fname}: MISSING (will be computed after file is created)")

print(f"\nFreeze A artifacts saved to: {FREEZE_DIR}")
print("Run predict.py to generate rankings.")
print("Run metadata_validator.py to validate incoming lab data.")
