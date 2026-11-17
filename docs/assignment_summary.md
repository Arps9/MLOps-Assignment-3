# Assignment 3 – Source-based summary

The assignment asks for model performance monitoring, data drift detection, anomaly detection, visualization of ML metrics, and threshold-based alerts.

## Metrics
- Accuracy, precision, recall or F1 when ground-truth labels are available
- Prediction volume
- Data drift score
- Anomaly count
- Prediction latency

## Architecture
ML Model/API exposes metrics → Prometheus scrapes time-series data → Grafana visualizes dashboards and alert status.

## Demonstration methods
- Drift: absolute difference between reference and current feature means.
- Anomalies: absolute z-score greater than 3.
- Alerts: accuracy < 0.85, drift > 0.20, anomaly count > 5, each sustained for 5 minutes.

## Limitation
The submitted PDF labels its dashboard and alert values as illustrative mock-up values, not live deployment measurements. This repository implements a runnable demonstration exporter and configuration; it does not claim production deployment.
