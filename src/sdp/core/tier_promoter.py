"""Tier promotion/demotion logic based on metrics."""

from typing import Optional

from sdp.core.tier_metrics import TierMetrics


class PromotionRule:
    """Single promotion rule configuration."""

    def __init__(self, min_successes: int, min_success_rate: float, promotes_to: str):
        """Initialize promotion rule.

        Args:
            min_successes: Minimum successful attempts required
            min_success_rate: Minimum success rate required (0.0-1.0)
            promotes_to: Target tier after promotion
        """
        self.min_successes = min_successes
        self.min_success_rate = min_success_rate
        self.promotes_to = promotes_to


# Promotion rules: T3 -> T2 -> T1 -> T0
PROMOTION_RULES = {
    "T3": PromotionRule(min_successes=10, min_success_rate=0.80, promotes_to="T2"),
    "T2": PromotionRule(min_successes=20, min_success_rate=0.85, promotes_to="T1"),
    "T1": PromotionRule(min_successes=30, min_success_rate=0.90, promotes_to="T0"),
}

# Demotion threshold
DEMOTION_THRESHOLD = 3  # consecutive failures


def check_promotion(metrics: TierMetrics) -> Optional[str]:
    """Check if workstream is eligible for tier promotion.

    Args:
        metrics: Current tier metrics

    Returns:
        New tier if promotion eligible, None otherwise
    """
    tier = metrics.current_tier
    if tier not in PROMOTION_RULES:
        return None  # T0 cannot be promoted

    rule = PROMOTION_RULES[tier]
    if (
        metrics.successful_attempts >= rule.min_successes
        and metrics.success_rate >= rule.min_success_rate
    ):
        return rule.promotes_to

    return None


def check_demotion(metrics: TierMetrics) -> Optional[str]:
    """Check if workstream should be demoted.

    Args:
        metrics: Current tier metrics

    Returns:
        New tier if demotion needed, None otherwise
    """
    if metrics.consecutive_failures >= DEMOTION_THRESHOLD:
        # Demote one tier down
        tier_order = ["T0", "T1", "T2", "T3"]
        current_idx = tier_order.index(metrics.current_tier)
        if current_idx < len(tier_order) - 1:
            return tier_order[current_idx + 1]

    return None


def check_tier_change(metrics: TierMetrics) -> Optional[str]:
    """Check if tier should change (promotion or demotion).

    Args:
        metrics: Current tier metrics

    Returns:
        New tier if change needed, None otherwise
    """
    # Check demotion first (higher priority)
    new_tier = check_demotion(metrics)
    if new_tier:
        return new_tier

    # Check promotion
    return check_promotion(metrics)
