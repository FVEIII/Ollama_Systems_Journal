class Var4DSurrogateBackend:
    def get_fields(self, lat: float, lon: float, date_range: list[str]):
        return {
            "model": "4DVar-surrogate-stub",
            "grid": "2km",
            "temp_c": [21.9, 22.0, 22.4],
            "wind_ms": [3.0, 3.1, 3.6],
            "precip_mm": [0.1, 1.2, 0.3],
            "uncertainty": {"temp_c": 0.4, "wind_ms": 0.3, "precip_mm": 0.2},
            "meta": {"lat": lat, "lon": lon, "dates": date_range},
        }
