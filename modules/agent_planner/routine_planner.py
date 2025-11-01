from importlib import import_module
from dataclasses import dataclass
from .trace_logger import TraceLogger

@dataclass
class PlanStep:
    name: str
    fn: str   # "package.module:function"
    args: dict

class RoutinePlanner:
    def __init__(self, log_dir: str):
        self.logger = TraceLogger(log_dir)

    def _resolve(self, dotted: str):
        mod, fn = dotted.split(":")
        return getattr(import_module(mod), fn)

    def run(self, steps: list[PlanStep]):
        results = {}
        for i, step in enumerate(steps, 1):
            fn = self._resolve(step.fn)
            out = fn(**step.args, context=results)
            rec = {"step": i, "name": step.name, "fn": step.fn, "args": step.args, "out": out}
            self.logger.write(rec)
            results[step.name] = out
        return results
