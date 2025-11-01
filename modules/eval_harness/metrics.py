def task_success(output: dict) -> float:
    needed = {"weather", "logistics"}
    return float(needed.issubset(output.keys()))
