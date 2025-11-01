def apply_policies(env: dict, inventory: float = 1000.0, port_delay_days: int = 0, subsidy_per_kg: float = 0.0):
    rain = sum(env["precip_mm"])
    defect_rate = min(0.05 + 0.005 * rain, 0.25)
    usable = inventory * (1 - defect_rate)
    return {"usable_kg": round(usable, 2), "defect_rate": round(defect_rate, 3),
            "port_delay_days": port_delay_days, "subsidy_per_kg": subsidy_per_kg}
