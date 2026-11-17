# MLOps Assignment 3 – Model Monitoring and Alerting

**Name:** Shreyash Pawar  
**Roll No.:** 31  
**PRN:** 22311673

## Assignment scope

This project demonstrates monitoring and alerting for:
- Model performance (accuracy)
- Data drift score
- Anomaly count
- Prediction volume
- Prediction latency

The architecture follows the assignment: **ML application → Prometheus → Grafana dashboards and alert rules**.

## Repository structure

```text
MLOps-Assignment-3/
├── app/
│   └── monitoring_app.py
├── prometheus/
│   ├── prometheus.yml
│   └── alert_rules.yml
├── grafana/
│   ├── dashboards/
│   │   └── mlops-monitoring.json
│   └── provisioning/
│       ├── datasources/prometheus.yml
│       └── dashboards/dashboard.yml
├── docs/
├── screenshots/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md
```

## Option A: Run Python exporter locally

Requires Python 3.10+.

```cmd
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python app/monitoring_app.py
```

Open `http://localhost:8000/metrics` to see Prometheus metrics. Keep this terminal running.

## Option B: Run full Prometheus + Grafana stack with Docker

Requires Docker Desktop.

From the repository root:

```cmd
docker compose up --build -d
```

Open:
- ML metrics: http://localhost:8000/metrics
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

Default Grafana login for a fresh local container is `admin` / `admin`; Grafana may ask you to change the password on first login.

Stop the stack:

```cmd
docker compose down
```

## Prometheus metrics

| Metric | Meaning |
|---|---|
| `ml_prediction_total` | Total predictions served |
| `ml_model_accuracy` | Accuracy on the demonstration test batch |
| `ml_data_drift_score` | Absolute mean difference for `mean radius` |
| `ml_anomaly_count` | Number of z-score anomalies in latest batch |
| `ml_prediction_latency_seconds` | Prediction latency histogram |
| `ml_monitoring_batch_total` | Monitoring batches processed |

## Alert thresholds

The Prometheus rules in `prometheus/alert_rules.yml` follow the assignment thresholds:
- Accuracy below 0.85 for 5 minutes
- Drift score above 0.20 for 5 minutes
- Anomaly count above 5 for 5 minutes

Prometheus evaluates the rules. The project does not configure email or external notification delivery; the alerts can be inspected in Prometheus under **Alerts**.

## Important interpretation

The app uses the built-in Breast Cancer Wisconsin dataset and synthetic feature shifts to demonstrate monitoring behavior. It is not a live production deployment, and the monitoring values are demonstrations. The simple mean-difference drift score and z-score anomaly detector are educational examples, not universal production methods. Model accuracy is only measurable here because the demonstration test labels are available.

## Assignment architecture

```text
ML Model / API
      |
      | exposes /metrics on port 8000
      v
  Prometheus (9090)
      |
      | scrapes time-series metrics
      v
    Grafana (3000)
      |
      +--> Dashboard panels
      +--> Prometheus alert rules
```

## GitHub upload

Create an empty GitHub repository, then run these commands in this folder:

```cmd
git init
git add .
git commit -m "Add MLOps Assignment 3 monitoring and alerting"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/MLOps-Assignment-3.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username.
