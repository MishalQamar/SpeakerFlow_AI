import datetime

from pydantic import BaseModel, EmailStr, PositiveInt

from speakerflow_ai.models import Address, SpeakingRequestStatus


class SpeakingRequestDetails(BaseModel):
    id: str
    event_time: datetime.datetime
    address: Address
    topic: str
    duration_in_minutes: PositiveInt
    requester_email: EmailStr
    status: SpeakingRequestStatus


class SpeakingRequestList(BaseModel):
    results: list[SpeakingRequestDetails]
