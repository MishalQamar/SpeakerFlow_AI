import datetime

from pydantic import BaseModel, EmailStr, PositiveInt

from speakerflow_ai.models import Address


class SubmitSpeakingRequest(BaseModel):
    event_time: datetime.datetime
    address: Address
    topic: str
    duration_in_minutes: PositiveInt
    requester_email: EmailStr
