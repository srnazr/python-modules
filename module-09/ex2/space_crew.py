from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, model_validator, ValidationError


class Rank(str, Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=2, max_length=50)
    rank: Rank
    age: int = Field(..., ge=18, le=80)
    specialization: str = Field(..., min_length=3, max_length=30)
    years_experience: int = Field(..., ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(..., min_length=5, max_length=15)
    mission_name: str = Field(..., min_length=3, max_length=100)
    destination: str = Field(..., min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(..., ge=1, le=3650)
    crew: list[CrewMember] = Field(..., min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(..., ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def check_mission_safety(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")

        has_commander_or_captain = False
        for crew_member in self.crew:
            if crew_member.rank == Rank.commander:
                has_commander_or_captain = True
            if crew_member.rank == Rank.captain:
                has_commander_or_captain = True

        if not has_commander_or_captain:
            raise ValueError(
                "Mission must have at least one Commander or Captain"
            )

        if self.duration_days > 365:
            experienced_count = 0
            for crew_member in self.crew:
                if crew_member.years_experience >= 5:
                    experienced_count = experienced_count + 1

            required_count = len(self.crew) * 0.5
            if experienced_count < required_count:
                raise ValueError(
                    "Long missions (> 365 days) need 50% experienced crew "
                    "(5+ years)"
                )

        for crew_member in self.crew:
            if not crew_member.is_active:
                raise ValueError("All crew members must be active")

        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("=" * 41)

    valid_mission = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date="2024-06-01T08:00:00",
        duration_days=900,
        budget_millions=2500.0,
        crew=[
            CrewMember(
                member_id="CM001",
                name="Sarah Connor",
                rank=Rank.commander,
                age=42,
                specialization="Mission Command",
                years_experience=20,
            ),
            CrewMember(
                member_id="CM002",
                name="John Smith",
                rank=Rank.lieutenant,
                age=35,
                specialization="Navigation",
                years_experience=10,
            ),
            CrewMember(
                member_id="CM003",
                name="Alice Johnson",
                rank=Rank.officer,
                age=29,
                specialization="Engineering",
                years_experience=6,
            ),
        ],
    )

    print("Valid mission created:")
    print("Mission: " + valid_mission.mission_name)
    print("ID: " + valid_mission.mission_id)
    print("Destination: " + valid_mission.destination)
    print("Duration: " + str(valid_mission.duration_days) + " days")
    print("Budget: $" + str(valid_mission.budget_millions) + "M")
    print("Crew size: " + str(len(valid_mission.crew)))
    print("Crew members:")

    for crew_member in valid_mission.crew:
        line = "- " + crew_member.name
        line = line + " (" + crew_member.rank.value + ")"
        line = line + "- " + crew_member.specialization
        print(line)

    print("=" * 41)

    try:
        invalid_mission = SpaceMission(
            mission_id="M2024_MOON",
            mission_name="Moon Base Supply Run",
            destination="Moon",
            launch_date="2024-07-01T08:00:00",
            duration_days=30,
            budget_millions=50.0,
            crew=[
                CrewMember(
                    member_id="CM004",
                    name="Bob Miller",
                    rank=Rank.cadet,
                    age=24,
                    specialization="Logistics",
                    years_experience=1,
                ),
            ],
        )
        print(invalid_mission)
    except ValidationError as error:
        print("Expected validation error:")
        first_error = error.errors()[0]
        print(first_error["msg"])


if __name__ == "__main__":
    main()
