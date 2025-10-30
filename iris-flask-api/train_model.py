import json
import joblib
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

def main():
    iris = load_iris()
    X = pd.DataFrame(iris.data, columns=iris.feature_names)
    y = pd.Series(iris.target, name='species')

    print("=== EDA: head ===")
    print(X.head().to_string(index=False))
    print("\n=== EDA: describe ===")
    print(X.describe().to_string())
    print("\n=== EDA: target distribution ===")
    print(y.value_counts().to_string())

    print("\n=== Missing values per column ===")
    print(X.isnull().sum().to_string())

    X_train, X_test, y_train, y_test = train_test_split(
        X.values, y.values, test_size=0.2, random_state=42, stratify=y.values
    )

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", RandomForestClassifier(n_estimators=100, random_state=42))
    ])

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=iris.target_names, output_dict=True)

    print("\n=== Evaluation ===")
    print(f"Accuracy: {acc:.4f}")
    print(classification_report(y_test, y_pred, target_names=iris.target_names))

    model_path = "model.joblib"
    joblib.dump({
        "model": pipeline,
        "target_names": iris.target_names.tolist(),
        "feature_names": iris.feature_names
    }, model_path)
    print(f"\nSaved model pipeline to: {model_path}")

    metrics = {"accuracy": float(acc), "classification_report": report}
    with open("metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)
    print("Saved metrics to metrics.json")

if __name__ == "__main__":
    main()
