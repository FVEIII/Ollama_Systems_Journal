from .policies import apply_policies

def plan_logistics(env: dict, context: dict):
    result = apply_policies(env, inventory=1000.0, port_delay_days=1, subsidy_per_kg=0.10)
    return {"env_model": env["model"], "summary": result}
