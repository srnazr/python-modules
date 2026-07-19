from datetime import datetime
from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
    station_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=1, max_length=50)
    crew_size: int = Field(..., ge=1, le=20)
    power_level: float = Field(..., ge=0.0, le=100.0)
    oxygen_level: float = Field(..., ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: str | None = Field(default=None, max_length=200)


def main() -> None:
    print("Space Station Data Validation")
    print("=" * 40)

    valid_station = SpaceStation(
        station_id="ISS001",
        name="International Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance="2024-01-15T10:30:00",
        is_operational=True,
    )

    print("Valid station created:")
    print("ID: " + valid_station.station_id)
    print("Name: " + valid_station.name)
    print("Crew: " + str(valid_station.crew_size) + " people")
    print("Power: " + str(valid_station.power_level) + "%")
    print("Oxygen: " + str(valid_station.oxygen_level) + "%")

    if valid_station.is_operational:
        print("Status: Operational")
    else:
        print("Status: Not Operational")

    print("=" * 40)

    try:
        invalid_station = SpaceStation(
            station_id="ISS002",
            name="Broken Station",
            crew_size=25,
            power_level=50.0,
            oxygen_level=50.0,
            last_maintenance="2024-01-15T10:30:00",
        )
        print(invalid_station)
    except ValidationError as error:
        print("Expected validation error:")
        first_error = error.errors()[0]
        print(first_error["msg"])


if __name__ == "__main__":
    main()
