#!/bin/bash
# Serve metrics dashboard locally

set -e

echo "📊 Consensus Metrics Dashboard"
echo "==============================="
echo ""

# Собираем метрики
echo "Collecting metrics..."
python scripts/metrics_collector.py

# Запускаем сервер
echo ""
echo "Starting dashboard server..."
echo "Dashboard: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop"
echo ""

cd dashboard
python3 -m http.server 8000
