from typing import Dict, Any, Optional, List

def rainfall_shock(env: Dict[str, Any],
                   context: Optional[Dict[str, Any]] = None,
                   pct_increase: float = 0.5) -> Dict[str, Any]:
    """
    Multiply precipitation values by (1 + pct_increase).
    Adds a 'shock' tag into env['meta'].
    """
    out = dict(env)
    precip: List[float] = list(env.get("precip_mm", []))
    out["precip_mm"] = [round(x * (1.0 + pct_increase), 2) for x in precip]
    meta = dict(env.get("meta", {}))
    meta["shock"] = f"rainfall+{int(pct_increase * 100)}%"
    out["meta"] = meta
    return out
