from dataclasses import dataclass

@dataclass
class Scenario:
    name: str

def basic():
    return Scenario(name="basic")
