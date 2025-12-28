# Consensus Metrics Guide

Система автоматического сбора и визуализации метрик для AI-агентов.

## Зачем нужны метрики?

В отличие от традиционного time tracking, метрики для AI workflow фокусируются на:

- **Latency** - скорость выполнения агентов (не часы работы)
- **Cost** - расход токенов и стоимость (не зарплата)
- **Quality** - количество итераций и vetoes (не velocity)
- **Efficiency** - bottlenecks и idle time (не burndown)

## Быстрый старт

### 1. Сбор метрик вручную

```bash
# Запустить collector
python scripts/metrics_collector.py

# Результаты сохраняются в:
# - metrics/metrics.json (для dashboard)
# - metrics/metrics.prom (для Prometheus)
```

### 2. Просмотр dashboard

```bash
# Открыть локальный dashboard
cd dashboard
python -m http.server 8000

# Открыть в браузере
open http://localhost:8000
```

### 3. Автоматический сбор через GitHub Actions

Метрики собираются автоматически при:
- Создании/обновлении артефактов
- Каждый час (по расписанию)
- Вручную через Actions → "Collect Consensus Metrics"

Dashboard публикуется на GitHub Pages: `https://YOUR_USERNAME.github.io/consensus/`

## Собираемые метрики

### Epic Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `epic_duration_seconds` | Gauge | Общая продолжительность epic |
| `epic_iterations` | Counter | Количество итераций до консенсуса |
| `epic_vetoes` | Counter | Количество vetoes |
| `epic_cost_usd` | Gauge | Стоимость в долларах |
| `epic_consensus_achieved` | Gauge | 1 если консенсус достигнут, 0 иначе |
| `epic_agents_completed` | Gauge | Количество завершённых агентов |

### Agent Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `agent_duration_seconds` | Histogram | Время выполнения агента |
| `agent_artifacts_created` | Counter | Количество созданных артефактов |
| `agent_vetoes_issued` | Counter | Количество выданных vetoes |

### Summary Metrics

| Metric | Description |
|--------|-------------|
| `total_epics` | Всего epics |
| `completed_epics` | Завершённые epics |
| `avg_iterations` | Среднее количество итераций |
| `avg_vetoes` | Среднее количество vetoes |
| `total_cost_usd` | Общая стоимость |

## Dashboard Features

### 1. Summary Cards

Краткий обзор:
- Total Epics
- Completed (с % success rate)
- Avg Iterations (качество с первого раза)
- Avg Vetoes (срабатывание quality gates)
- Total Cost

### 2. Charts

**Epic Status Distribution** (Doughnut)
- Показывает распределение epics по статусам

**Agent Performance** (Bar)
- Количество завершённых задач по каждому агенту
- Помогает найти bottleneck

**Iterations vs Vetoes** (Bubble)
- Корреляция между итерациями и vetoes
- Размер пузыря = стоимость

**Cost Breakdown** (Line)
- Динамика стоимости по epics
- Тренд расходов

### 3. Epics List

Таблица всех epics с:
- Status badge
- Current agent
- Iterations, Vetoes, Cost
- Consensus status

## Интерпретация метрик

### ✅ Хорошие показатели

```yaml
avg_iterations: 1.2        # Консенсус с первого раза
avg_vetoes: 0.3           # Мало vetoes
epic_duration: < 20min    # Быстрое выполнение
cost_per_epic: < $3       # Эффективное использование токенов
```

### ⚠️ Требует внимания

```yaml
avg_iterations: > 2       # Частые переделки
avg_vetoes: > 2          # Много quality gate срабатываний
epic_duration: > 60min   # Медленное выполнение
cost_per_epic: > $10     # Высокий расход токенов
```

### 🔍 Что смотреть при проблемах

**Много итераций:**
- Проверьте качество промптов
- Возможно, недостаточно контекста в epic.md
- Architect часто vetoes → требования нечёткие

**Много vetoes:**
- Проверьте engineering_principles в промптах
- Возможно, нужно обучить модель на примерах
- Часто одни и те же ошибки → добавьте в quick prompts

**Высокая стоимость:**
- Проверьте, используются ли quick prompts
- Возможно, слишком большой контекст
- Рассмотрите переход на Sonnet для routine tasks

**Медленное выполнение:**
- Проверьте bottleneck в Agent Performance chart
- Возможно, можно распараллелить (QA + Security)
- Используйте faster models где возможно

## Prometheus Integration

Для долгосрочного мониторинга можно настроить Prometheus:

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'consensus'
    static_configs:
      - targets: ['localhost:9090']
    file_sd_configs:
      - files:
        - /path/to/consensus/metrics/metrics.prom
```

Затем визуализировать в Grafana:

```promql
# Avg epic duration
avg(consensus_epic_duration_seconds)

# Success rate
consensus_completed_epics / consensus_total_epics

# Cost trend
rate(consensus_epic_cost_usd[1h])
```

## GitHub Actions Integration

Метрики автоматически:

1. **Собираются** при push в `docs/specs/*/consensus/`
2. **Коммитятся** в `metrics/`
3. **Публикуются** на GitHub Pages
4. **Комментируются** в epic issues

Пример комментария в issue:

```markdown
## ✅ Epic Metrics Update

**Status:** implementation
**Progress:** 4/6 agents completed
**Current Agent:** developer

### Quality Metrics
- **Iterations:** 2
- **Vetoes:** 1
- **Consensus:** ⚠️ Vetoes present

### Performance
- **Duration:** 15.3 minutes
- **Cost:** $2.45

### Completed Agents
- ✅ analyst
- ✅ architect
- ✅ tech_lead
- ✅ developer

---
📊 [View full dashboard](https://your-username.github.io/consensus/)
```

## Custom Metrics

Для добавления кастомных метрик:

```python
# scripts/metrics_collector.py

@dataclass
class AgentMetrics:
    # ... существующие поля ...

    # Добавьте новое поле
    custom_metric: Optional[float] = None

# В методе collect_agent_metrics:
custom_value = self.calculate_custom_metric(epic_id, agent)
metrics.append(AgentMetrics(
    # ...
    custom_metric=custom_value
))
```

Обновите dashboard:

```javascript
// dashboard/index.html

// Добавьте новый chart
function renderCustomChart() {
    const data = metricsData.epics.map(epic => epic.custom_metric);
    // ... chart code
}
```

## Troubleshooting

### Metrics не собираются

```bash
# Проверьте структуру
ls -la docs/specs/epic_*/consensus/

# Запустите вручную с debug
python scripts/metrics_collector.py
```

### Dashboard не загружается

```bash
# Проверьте metrics.json
cat metrics/metrics.json

# Запустите локальный сервер
cd dashboard && python -m http.server 8000
```

### GitHub Actions fails

- Проверьте Python version (требуется 3.11+)
- Проверьте права на push в repo
- Проверьте, включены ли GitHub Pages в Settings

## Best Practices

1. **Собирайте метрики регулярно** - настройте GitHub Actions
2. **Анализируйте тренды** - смотрите на изменения, не абсолютные значения
3. **Оптимизируйте на основе данных** - если avg_iterations растёт, улучшайте промпты
4. **Следите за стоимостью** - переключайтесь на quick prompts и cheaper models где возможно
5. **Используйте для обучения** - успешные epics как примеры для новых

---

**См. также:**
- [MODELS.md](../MODELS.md) - Рекомендации по моделям
- [PROTOCOL.md](../PROTOCOL.md) - Consensus protocol
- [Dashboard](https://your-username.github.io/consensus/) - Live metrics
