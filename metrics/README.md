# Metrics Data

This directory contains automatically collected metrics from consensus workflow.

## Files

- `metrics.json` - JSON format for dashboard
- `metrics.prom` - Prometheus format for monitoring

## Usage

### View Dashboard

```bash
./scripts/serve_dashboard.sh
```

Open http://localhost:8000

### Update Metrics

```bash
python scripts/metrics_collector.py
```

Metrics are automatically updated by GitHub Actions on every push to `docs/specs/*/consensus/`.

---

See [docs/METRICS.md](../docs/METRICS.md) for full documentation.
