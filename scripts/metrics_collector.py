#!/usr/bin/env python3
"""
Consensus Workflow Metrics Collector

Собирает метрики из артефактов и логирует в формате Prometheus.
"""

import json
import os
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import re


@dataclass
class AgentMetrics:
    """Метрики одного агента"""
    agent: str
    epic_id: str
    status: str  # completed, vetoed, in_progress
    duration_seconds: Optional[float] = None
    tokens_input: Optional[int] = None
    tokens_output: Optional[int] = None
    artifacts_created: int = 0
    vetoes_issued: int = 0
    timestamp: str = ""


@dataclass
class EpicMetrics:
    """Метрики всего epic"""
    epic_id: str
    title: str
    status: str  # requirements, architecture, implementation, testing, deployment, done
    total_duration_seconds: float
    agents_completed: List[str]
    current_agent: Optional[str]
    iterations: int
    total_vetoes: int
    total_cost_usd: float
    consensus_achieved: bool
    started_at: str
    completed_at: Optional[str] = None


class MetricsCollector:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.specs_dir = self.base_path / "docs" / "specs"
        self.metrics_dir = self.base_path / "metrics"
        self.metrics_dir.mkdir(exist_ok=True)

    def collect_all_epics(self) -> List[EpicMetrics]:
        """Собрать метрики по всем эпикам"""
        epics = []

        if not self.specs_dir.exists():
            return epics

        for epic_dir in self.specs_dir.glob("epic_*"):
            if epic_dir.is_dir():
                epic_metrics = self.collect_epic_metrics(epic_dir)
                if epic_metrics:
                    epics.append(epic_metrics)

        return epics

    def collect_epic_metrics(self, epic_dir: Path) -> Optional[EpicMetrics]:
        """Собрать метрики одного epic"""
        epic_id = epic_dir.name

        # Читаем epic.md для получения title
        epic_file = epic_dir / "epic.md"
        title = epic_id
        if epic_file.exists():
            content = epic_file.read_text()
            match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if match:
                title = match.group(1).strip()

        consensus_dir = epic_dir / "consensus"
        if not consensus_dir.exists():
            return None

        # Собираем метрики агентов
        agent_metrics = self.collect_agent_metrics(epic_id, consensus_dir)

        # Определяем статус epic
        status = self.determine_epic_status(agent_metrics)

        # Подсчёт vetoes
        total_vetoes = sum(m.vetoes_issued for m in agent_metrics)

        # Определяем текущего агента
        current_agent = self.determine_current_agent(agent_metrics)

        # Считаем итерации
        iterations = self.count_iterations(consensus_dir)

        # Время
        started_at, completed_at, total_duration = self.calculate_duration(consensus_dir, agent_metrics)

        # Стоимость (примерная, если есть данные о токенах)
        total_cost = self.estimate_cost(agent_metrics)

        return EpicMetrics(
            epic_id=epic_id,
            title=title,
            status=status,
            total_duration_seconds=total_duration,
            agents_completed=[m.agent for m in agent_metrics if m.status == "completed"],
            current_agent=current_agent,
            iterations=iterations,
            total_vetoes=total_vetoes,
            total_cost_usd=total_cost,
            consensus_achieved=status == "done" and total_vetoes == 0,
            started_at=started_at,
            completed_at=completed_at
        )

    def collect_agent_metrics(self, epic_id: str, consensus_dir: Path) -> List[AgentMetrics]:
        """Собрать метрики всех агентов в epic"""
        metrics = []

        artifacts_dir = consensus_dir / "artifacts"
        messages_dir = consensus_dir / "messages" / "inbox"

        agents = ["analyst", "architect", "tech_lead", "developer", "qa", "devops"]

        for agent in agents:
            # Проверяем наличие артефактов
            agent_artifact = self.find_agent_artifact(artifacts_dir, agent)

            if agent_artifact:
                # Агент завершил работу
                status = "completed"
                artifacts_created = 1

                # Проверяем на vetoes
                vetoes = self.count_vetoes(messages_dir, agent)

                # Время создания артефакта
                timestamp = datetime.fromtimestamp(agent_artifact.stat().st_mtime).isoformat()

                metrics.append(AgentMetrics(
                    agent=agent,
                    epic_id=epic_id,
                    status=status,
                    artifacts_created=artifacts_created,
                    vetoes_issued=vetoes,
                    timestamp=timestamp
                ))
            else:
                # Проверяем, есть ли задача для этого агента
                agent_inbox = messages_dir / agent if messages_dir.exists() else None
                if agent_inbox and agent_inbox.exists() and list(agent_inbox.glob("*.json")):
                    metrics.append(AgentMetrics(
                        agent=agent,
                        epic_id=epic_id,
                        status="in_progress",
                        timestamp=datetime.now().isoformat()
                    ))

        return metrics

    def find_agent_artifact(self, artifacts_dir: Path, agent: str) -> Optional[Path]:
        """Найти артефакт агента"""
        if not artifacts_dir.exists():
            return None

        # Маппинг агент -> артефакт
        artifact_map = {
            "analyst": "requirements.json",
            "architect": "architecture.json",
            "tech_lead": "implementation.json",
            "developer": "implementation.json",
            "qa": "test_results.md",
            "devops": "deployment.json"
        }

        artifact_name = artifact_map.get(agent)
        if not artifact_name:
            return None

        artifact_path = artifacts_dir / artifact_name
        return artifact_path if artifact_path.exists() else None

    def count_vetoes(self, messages_dir: Path, agent: str) -> int:
        """Подсчитать количество vetoes от агента"""
        if not messages_dir.exists():
            return 0

        vetoes = 0
        for message_file in messages_dir.rglob("*.json"):
            try:
                with open(message_file) as f:
                    msg = json.load(f)
                    if msg.get("r") == agent and msg.get("st") == "veto":
                        vetoes += 1
            except:
                continue

        return vetoes

    def determine_epic_status(self, agent_metrics: List[AgentMetrics]) -> str:
        """Определить статус epic по завершённым агентам"""
        completed = [m.agent for m in agent_metrics if m.status == "completed"]

        if "devops" in completed:
            return "done"
        elif "qa" in completed:
            return "deployment"
        elif "developer" in completed:
            return "testing"
        elif "tech_lead" in completed:
            return "implementation"
        elif "architect" in completed:
            return "planning"
        elif "analyst" in completed:
            return "architecture"
        else:
            return "requirements"

    def determine_current_agent(self, agent_metrics: List[AgentMetrics]) -> Optional[str]:
        """Определить текущего активного агента"""
        in_progress = [m.agent for m in agent_metrics if m.status == "in_progress"]
        if in_progress:
            return in_progress[0]

        # Если никто не in_progress, возвращаем следующего после последнего completed
        completed = [m.agent for m in agent_metrics if m.status == "completed"]
        agent_sequence = ["analyst", "architect", "tech_lead", "developer", "qa", "devops"]

        for i, agent in enumerate(agent_sequence):
            if agent not in completed:
                return agent

        return None

    def count_iterations(self, consensus_dir: Path) -> int:
        """Подсчитать количество итераций"""
        decision_log_dir = consensus_dir / "decision_log"
        if not decision_log_dir.exists():
            return 1

        # Ищем упоминания итераций в логах
        max_iteration = 1
        for log_file in decision_log_dir.glob("*.md"):
            content = log_file.read_text()
            matches = re.findall(r'iteration[:\s]+(\d+)', content, re.IGNORECASE)
            if matches:
                max_iteration = max(max_iteration, max(int(m) for m in matches))

        return max_iteration

    def calculate_duration(self, consensus_dir: Path, agent_metrics: List[AgentMetrics]) -> tuple:
        """Рассчитать продолжительность epic"""
        artifacts_dir = consensus_dir / "artifacts"

        if not artifacts_dir.exists() or not agent_metrics:
            return datetime.now().isoformat(), None, 0.0

        # Находим самый ранний и поздний артефакты
        artifacts = list(artifacts_dir.glob("*"))
        if not artifacts:
            return datetime.now().isoformat(), None, 0.0

        mtimes = [a.stat().st_mtime for a in artifacts]
        started_at = datetime.fromtimestamp(min(mtimes)).isoformat()

        completed_agents = [m for m in agent_metrics if m.status == "completed"]
        if len(completed_agents) == 6:  # Все агенты завершили
            completed_at = datetime.fromtimestamp(max(mtimes)).isoformat()
            duration = max(mtimes) - min(mtimes)
        else:
            completed_at = None
            duration = time.time() - min(mtimes)

        return started_at, completed_at, duration

    def estimate_cost(self, agent_metrics: List[AgentMetrics]) -> float:
        """Примерная оценка стоимости"""
        # Примерные цены Claude Opus 4: $15/1M input, $75/1M output
        total_cost = 0.0

        # Если есть реальные данные о токенах
        for metric in agent_metrics:
            if metric.tokens_input and metric.tokens_output:
                cost = (metric.tokens_input / 1_000_000 * 15) + \
                       (metric.tokens_output / 1_000_000 * 75)
                total_cost += cost
            elif metric.status == "completed":
                # Примерная оценка: 3000 токенов input, 5000 output на агента
                total_cost += (3000 / 1_000_000 * 15) + (5000 / 1_000_000 * 75)

        return round(total_cost, 2)

    def export_prometheus_metrics(self, epics: List[EpicMetrics]) -> str:
        """Экспорт метрик в формате Prometheus"""
        lines = []

        # Epic metrics
        for epic in epics:
            labels = f'epic_id="{epic.epic_id}",status="{epic.status}"'

            lines.append(f'consensus_epic_duration_seconds{{{labels}}} {epic.total_duration_seconds}')
            lines.append(f'consensus_epic_iterations{{{labels}}} {epic.iterations}')
            lines.append(f'consensus_epic_vetoes{{{labels}}} {epic.total_vetoes}')
            lines.append(f'consensus_epic_cost_usd{{{labels}}} {epic.total_cost_usd}')
            lines.append(f'consensus_epic_consensus_achieved{{{labels}}} {int(epic.consensus_achieved)}')
            lines.append(f'consensus_epic_agents_completed{{{labels}}} {len(epic.agents_completed)}')

        # Summary metrics
        total_epics = len(epics)
        completed_epics = len([e for e in epics if e.status == "done"])
        avg_iterations = sum(e.iterations for e in epics) / total_epics if total_epics > 0 else 0
        avg_vetoes = sum(e.total_vetoes for e in epics) / total_epics if total_epics > 0 else 0

        lines.append(f'consensus_total_epics {total_epics}')
        lines.append(f'consensus_completed_epics {completed_epics}')
        lines.append(f'consensus_avg_iterations {avg_iterations:.2f}')
        lines.append(f'consensus_avg_vetoes {avg_vetoes:.2f}')

        return "\n".join(lines)

    def export_json(self, epics: List[EpicMetrics]) -> str:
        """Экспорт метрик в JSON"""
        data = {
            "timestamp": datetime.now().isoformat(),
            "epics": [asdict(epic) for epic in epics],
            "summary": {
                "total_epics": len(epics),
                "completed_epics": len([e for e in epics if e.status == "done"]),
                "in_progress_epics": len([e for e in epics if e.status != "done"]),
                "avg_iterations": sum(e.iterations for e in epics) / len(epics) if epics else 0,
                "avg_vetoes": sum(e.total_vetoes for e in epics) / len(epics) if epics else 0,
                "total_cost_usd": sum(e.total_cost_usd for e in epics)
            }
        }
        return json.dumps(data, indent=2)

    def save_metrics(self, epics: List[EpicMetrics]):
        """Сохранить метрики в файлы"""
        # JSON для dashboard
        json_path = self.metrics_dir / "metrics.json"
        json_path.write_text(self.export_json(epics))

        # Prometheus для мониторинга
        prom_path = self.metrics_dir / "metrics.prom"
        prom_path.write_text(self.export_prometheus_metrics(epics))

        print(f"Metrics saved:")
        print(f"  JSON: {json_path}")
        print(f"  Prometheus: {prom_path}")


def main():
    collector = MetricsCollector()
    epics = collector.collect_all_epics()

    if not epics:
        print("No epics found")
        return

    collector.save_metrics(epics)

    # Вывод summary
    print(f"\n=== Summary ===")
    print(f"Total epics: {len(epics)}")
    print(f"Completed: {len([e for e in epics if e.status == 'done'])}")
    print(f"In progress: {len([e for e in epics if e.status != 'done'])}")
    print(f"Total cost: ${sum(e.total_cost_usd for e in epics):.2f}")

    print(f"\n=== Epics ===")
    for epic in epics:
        status_icon = "✅" if epic.status == "done" else "🔄"
        print(f"{status_icon} {epic.epic_id}: {epic.title}")
        print(f"   Status: {epic.status} | Iterations: {epic.iterations} | Vetoes: {epic.total_vetoes}")
        print(f"   Current: {epic.current_agent or 'None'} | Cost: ${epic.total_cost_usd:.2f}")


if __name__ == "__main__":
    main()
