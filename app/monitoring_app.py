"""
MLOps Assignment 3: Model Monitoring and Alerting
Prometheus metrics exporter with demonstration model, drift and anomaly metrics.

Run locally:
    python -m pip install -r requirements.txt
    python app/monitoring_app.py

Metrics endpoint: http://localhost:8000/metrics
These are synthetic demonstration observations, not live production measurements.
"""
import time
import random
import logging

import numpy as np
from prometheus_client import Counter, Gauge, Histogram, start_http_server
from sklearn.datasets import load_breast_cancer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("ml-monitoring")

# Prometheus metrics
PREDICTION_COUNT = Counter(
    "ml_prediction_total", "Total number of model predictions"
)
MODEL_ACCURACY = Gauge(
    "ml_model_accuracy", "Current demonstration model accuracy"
)
DATA_DRIFT_SCORE = Gauge(
    "ml_data_drift_score", "Absolute mean difference between reference and current feature"
)
ANOMALY_COUNT = Gauge(
    "ml_anomaly_count", "Number of anomalies in the latest demonstration batch"
)
PREDICTION_LATENCY = Histogram(
    "ml_prediction_latency_seconds",
    "Prediction latency in seconds",
    buckets=(0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0),
)
MONITORING_BATCH_COUNT = Counter(
    "ml_monitoring_batch_total", "Number of monitoring batches processed"
)

def calculate_simple_drift(reference, current):
    """Simple educational drift score: absolute difference in feature means."""
    return float(abs(np.mean(current) - np.mean(reference)))

def detect_anomalies(values, threshold=3.0):
    """Return a boolean mask for observations with absolute z-score > threshold."""
    values = np.asarray(values, dtype=float)
    mean = np.mean(values)
    std = np.std(values)
    if std == 0:
        return np.zeros(len(values), dtype=bool)
    z_scores = np.abs((values - mean) / std)
    return z_scores > threshold

def prepare_model():
    dataset = load_breast_cancer(as_frame=True)
    X, y = dataset.data, dataset.target
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    model = DecisionTreeClassifier(max_depth=4, random_state=42)
    model.fit(X_train, y_train)
    accuracy = accuracy_score(y_test, model.predict(X_test))
    return model, X_train, X_test, y_test, accuracy

def run_monitoring():
    model, X_train, X_test, y_test, accuracy = prepare_model()
    MODEL_ACCURACY.set(float(accuracy))
    reference = X_train["mean radius"].to_numpy()
    current_base = X_test["mean radius"].to_numpy()

    logger.info("Starting demonstration monitoring loop. Press Ctrl+C to stop.")
    batch_number = 0

    while True:
        batch_number += 1
        # Gradually add a small synthetic shift so drift alert behavior can be observed.
        shift = min(batch_number * 0.015, 0.35)
        current = current_base + shift

        drift_score = calculate_simple_drift(reference, current)
        anomalies = detect_anomalies(current)

        # Measure actual prediction latency on a small batch.
        sample = X_test.iloc[:10].copy()
        start = time.perf_counter()
        predictions = model.predict(sample)
        elapsed = time.perf_counter() - start
        PREDICTION_LATENCY.observe(elapsed / len(sample))
        PREDICTION_COUNT.inc(len(sample))
        MONITORING_BATCH_COUNT.inc()

        # Accuracy is measured against known test labels for this demonstration.
        batch_accuracy = accuracy_score(y_test.iloc[:len(predictions)], predictions)
        MODEL_ACCURACY.set(float(batch_accuracy))
        DATA_DRIFT_SCORE.set(drift_score)
        ANOMALY_COUNT.set(int(anomalies.sum()))

        logger.info(
            "batch=%d accuracy=%.3f drift=%.3f anomalies=%d predictions=%d",
            batch_number, batch_accuracy, drift_score, int(anomalies.sum()), len(predictions)
        )
        time.sleep(15)

if __name__ == "__main__":
    start_http_server(8000)
    logger.info("Prometheus metrics exposed at http://localhost:8000/metrics")
    try:
        run_monitoring()
    except KeyboardInterrupt:
        logger.info("Monitoring stopped.")
