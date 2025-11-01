from importlib import import_module

class WeatherAdapter:
    def __init__(self, backend_path: str):
        mod, cls = backend_path.split(":")
        self.backend = getattr(import_module(mod), cls)()

    def get_fields(self, lat: float, lon: float, date_range: list[str]):
        return self.backend.get_fields(lat=lat, lon=lon, date_range=date_range)

# dotted-path-friendly wrapper (so planner can call it directly)
def get_fields(lat: float, lon: float, date_range: list[str],
               backend_path: str, context: dict | None = None):
    return WeatherAdapter(backend_path).get_fields(lat=lat, lon=lon, date_range=date_range)
