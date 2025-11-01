class SpLIIFBackend:
    def get_fields(self, lat: float, lon: float, date_range: list[str]):
        return {
            "model": "SpLIIF-stub",
            "grid": "sub-km",
            "temp_c": [22.1, 21.8, 22.5],
            "wind_ms": [3.2, 2.9, 3.5],
            "precip_mm": [0.0, 1.4, 0.2],
            "uncertainty": {"temp_c": 0.6, "wind_ms": 0.4, "precip_mm": 0.3},
            "meta": {"lat": lat, "lon": lon, "dates": date_range},
        }
