import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, PositiveInt

from .address import Address


class SpeakingRequestStatus(str, Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class SpeakingRequest(BaseModel):
    id: str
    event_time: datetime.datetime
    address: Address
    topic: str
    duration_in_minutes: PositiveInt
    requester_email: EmailStr
    status: SpeakingRequestStatus

    def accept(self):
        self.status = SpeakingRequestStatus.ACCEPTED

    def reject(self):
        self.status = SpeakingRequestStatus.REJECTED
