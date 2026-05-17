from typing import Any, List, Optional


class Aeroplane:
    def __init__(
        self,
        icao24: str,
        callsign: Optional[str],
        country: str,
        altitude: Optional[float],
        velocity: Optional[float],
    ):
        self.icao24 = icao24
        self.callsign = callsign or "N/A"
        self.country = country
        self.altitude = altitude or 0.0
        self.velocity = velocity or 0.0

    @classmethod
    def cast_to_object_list(cls, data: List[List[Any]]) -> List["Aeroplane"]:
        """Преобразует данные OpenSky в список объектов Aeroplane."""
        aeroplanes = []
        for item in data:
            if len(item) >= 10:
                aeroplanes.append(
                    cls(
                        icao24=item[0],
                        callsign=item[1],
                        country=item[2],
                        altitude=item[7],
                        velocity=item[9],
                    )
                )
        return aeroplanes
