"""
Training pipeline for health risk models.

Usage:
    python -m risk_engine.train_pipeline
    python -m risk_engine.train_pipeline --samples 5000
"""

import argparse
import json
import os
from typing import Dict, Tuple

import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from config import settings


FEATURES = [
    "age",
    "bmi",
    "activity_score",
    "sleep_hours",
    "stress_level",
    "smoking",
    "family_history_score",
]


def _sigmoid(x: np.ndarray) -> np.ndarray:
    return 1 / (1 + np.exp(-x))


def generate_synthetic_dataset(n_samples: int = 4000, seed: int = 42) -> Tuple[np.ndarray, Dict[str, np.ndarray]]:
    rng = np.random.default_rng(seed)

    age = rng.integers(18, 81, size=n_samples)
    bmi = rng.normal(26, 5, size=n_samples).clip(16, 45)
    activity_score = rng.integers(1, 6, size=n_samples)
    sleep_hours = rng.normal(7, 1.5, size=n_samples).clip(3, 12)
    stress_level = rng.integers(1, 11, size=n_samples)
    smoking = rng.binomial(1, 0.22, size=n_samples)
    family_history_score = rng.integers(0, 4, size=n_samples)

    X = np.column_stack([
        age,
        bmi,
        activity_score,
        sleep_hours,
        stress_level,
        smoking,
        family_history_score,
    ]).astype(float)

    diabetes_p = _sigmoid(
        -9.0 + (0.055 * age) + (0.16 * bmi) - (0.30 * activity_score) + (0.50 * family_history_score)
    )
    hypertension_p = _sigmoid(
        -8.0 + (0.06 * age) + (0.12 * bmi) + (0.18 * stress_level) + (0.55 * smoking) + (0.30 * family_history_score)
    )
    cardiovascular_p = _sigmoid(
        -9.5 + (0.07 * age) + (0.09 * bmi) + (0.75 * smoking) + (0.45 * family_history_score) - (0.20 * activity_score)
    )

    labels = {
        "diabetes": rng.binomial(1, diabetes_p),
        "hypertension": rng.binomial(1, hypertension_p),
        "cardiovascular": rng.binomial(1, cardiovascular_p),
    }
    return X, labels


def train_and_save_models(samples: int = 4000) -> Dict:
    os.makedirs(settings.MODELS_DIR, exist_ok=True)
    X, labels = generate_synthetic_dataset(n_samples=samples)

    metrics = {}
    for condition, y in labels.items():
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        pipeline = Pipeline(
            steps=[
                ("scaler", StandardScaler()),
                ("clf", LogisticRegression(max_iter=500, class_weight="balanced", random_state=42)),
            ]
        )
        pipeline.fit(X_train, y_train)

        y_prob = pipeline.predict_proba(X_test)[:, 1]
        y_pred = (y_prob >= 0.5).astype(int)

        metrics[condition] = {
            "roc_auc": float(roc_auc_score(y_test, y_prob)),
            "f1": float(f1_score(y_test, y_pred)),
            "positive_rate_train": float(y_train.mean()),
            "positive_rate_test": float(y_test.mean()),
        }

        model_path = os.path.join(settings.MODELS_DIR, f"{condition}_model.pkl")
        joblib.dump(pipeline, model_path)

    metadata = {
        "feature_names": FEATURES,
        "samples": samples,
        "metrics": metrics,
        "model_type": "logistic_regression_pipeline",
    }

    metadata_path = os.path.join(settings.MODELS_DIR, "training_metadata.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    return metadata


def main() -> None:
    parser = argparse.ArgumentParser(description="Train health risk models.")
    parser.add_argument("--samples", type=int, default=4000, help="Number of synthetic training samples")
    args = parser.parse_args()

    result = train_and_save_models(samples=args.samples)
    print(json.dumps(result, indent=2))
    print(f"Saved models to: {settings.MODELS_DIR}")


if __name__ == "__main__":
    main()
