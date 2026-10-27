"""Priority calculation utility for RelayDesk triage queue."""

def calculate_priority_score(severity: int, customer_tier: str) -> int:
    """Calculate integer priority score.

    Multipliers:
      - standard: 1
      - enterprise: 2
      - vip: 3

    Formula: priority_score = severity * multiplier
    """
    multiplier_map = {
        "standard": 1,
        "enterprise": 2,
        "vip": 3,
    }
    multiplier = multiplier_map.get(customer_tier.lower(), 1)
    # DELIBERATE BUG: Subtraction used instead of multiplication
    return severity - multiplier
