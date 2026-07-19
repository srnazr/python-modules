from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, model_validator, ValidationError


class ContactType(str, Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(..., min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(..., min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(..., ge=0.0, le=10.0)
    duration_minutes: int = Field(..., ge=1, le=1440)
    witness_count: int = Field(..., ge=1, le=100)
    message_received: str | None = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def check_business_rules(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError(
                "Contact ID must start with 'AC' (Alien Contact)"
            )

        if self.contact_type == ContactType.physical:
            if not self.is_verified:
                raise ValueError("Physical contact reports must be verified")

        if self.contact_type == ContactType.telepathic:
            if self.witness_count < 3:
                raise ValueError(
                    "Telepathic contact requires at least 3 witnesses"
                )

        if self.signal_strength > 7.0:
            if self.message_received is None:
                raise ValueError(
                    "Strong signals (> 7.0) should include received messages"
                )

        return self


def main() -> None:
    print("Alien Contact Log Validation")
    print("=" * 38)

    valid_contact = AlienContact(
        contact_id="AC_2024_001",
        timestamp="2024-03-10T22:15:00",
        location="Area 51, Nevada",
        contact_type=ContactType.radio,
        signal_strength=8.5,
        duration_minutes=45,
        witness_count=5,
        message_received="Greetings from Zeta Reticuli",
    )

    print("Valid contact report:")
    print("ID: " + valid_contact.contact_id)
    print("Type: " + valid_contact.contact_type.value)
    print("Location: " + valid_contact.location)
    print("Signal: " + str(valid_contact.signal_strength) + "/10")
    print("Duration: " + str(valid_contact.duration_minutes) + " minutes")
    print("Witnesses: " + str(valid_contact.witness_count))

    if valid_contact.message_received is not None:
        print("Message: '" + valid_contact.message_received + "'")

    print("=" * 38)

    try:
        invalid_contact = AlienContact(
            contact_id="AC_2024_002",
            timestamp="2024-03-11T03:00:00",
            location="Roswell, New Mexico",
            contact_type=ContactType.telepathic,
            signal_strength=6.0,
            duration_minutes=20,
            witness_count=1,
        )
        print(invalid_contact)
    except ValidationError as error:
        print("Expected validation error:")
        first_error = error.errors()[0]
        print(first_error["msg"])


if __name__ == "__main__":
    main()
