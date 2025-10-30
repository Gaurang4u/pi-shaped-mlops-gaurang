from flask import Flask, request, jsonify
import joblib
import numpy as np
import os

MODEL_PATH = os.environ.get("MODEL_PATH", "model.joblib")
app = Flask(__name__)

try:
    saved = joblib.load(MODEL_PATH)
    model = saved["model"]
    target_names = saved.get("target_names", None)
    feature_names = saved.get("feature_names", None)
    app.logger.info(f"Loaded model from {MODEL_PATH}")
except Exception as e:
    model = None
    target_names = None
    feature_names = None
    app.logger.error(f"Failed to load model from {MODEL_PATH}: {e}")

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "service": "Iris classifier API",
        "endpoints": {
            "GET /health": "Health check",
            "POST /predict": {
                "description": "Predict iris species from features",
                "input_format_examples": [
                    {"input": [5.1, 3.5, 1.4, 0.2]},
                    {"input": [[5.1, 3.5, 1.4, 0.2], [6.0, 2.9, 4.5, 1.5]]}
                ],
                "feature_names": feature_names
            }
        }
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "model_loaded": model is not None})

def validate_and_format_input(data):
    if "input" not in data:
        raise ValueError("Missing 'input' key in JSON payload.")
    X = data["input"]
    if isinstance(X, list) and len(X) > 0 and not isinstance(X[0], list):
        X = [X]
    if not (isinstance(X, list) and all(isinstance(row, (list, tuple)) for row in X)):
        raise ValueError("'input' must be a list of 4 numeric features or list of such lists.")
    X_arr = np.array(X, dtype=float)
    if X_arr.ndim != 2 or X_arr.shape[1] != 4:
        raise ValueError("Each input sample must have 4 features.")
    return X_arr

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Invalid JSON payload"}), 400

    try:
        X = validate_and_format_input(data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    try:
        preds = model.predict(X)
        probs = model.predict_proba(X).tolist() if hasattr(model, "predict_proba") else None
        results = []
        for i, pred in enumerate(preds):
            species = target_names[pred] if target_names else int(pred)
            item = {"predicted_class": species, "predicted_label": int(pred)}
            if probs: item["probabilities"] = probs[i]
            results.append(item)
        return jsonify(results[0] if len(results) == 1 else results)
    except Exception as e:
        app.logger.exception("Prediction error")
        return jsonify({"error": f"Prediction failed: {e}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
