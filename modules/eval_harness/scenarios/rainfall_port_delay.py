from dataclasses import dataclass
from modules.logistics.policies import apply_policies

@dataclass
class Scenario:
    name: str
    description: str
    rain_factor: float
    port_delay_days: int

def rainfall_port_delay():
    """Simulate effect of heavy rainfall and port congestion."""
    scenario = Scenario(
        name="rainfall_port_delay",
        description="Impact of excess rainfall on usable inventory with added port delays",
        rain_factor=1.8,   # multiplier on baseline rainfall
        port_delay_days=4, # shipping congestion
    )

    # baseline environment
    base_env = {
        "precip_mm": [0.0, 1.4, 0.2],
        "model": "SpLIIF-stub",
    }

    # adjust rainfall by factor
    env = base_env.copy()
    env["precip_mm"] = [p * scenario.rain_factor for p in base_env["precip_mm"]]

    # compute logistics output
    result = apply_policies(env, inventory=1000.0, port_delay_days=scenario.port_delay_days)
    return {"scenario": scenario.name, "description": scenario.description, "result": result}
