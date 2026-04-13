from datetime import datetime
from typing import Any

from sqlalchemy import JSON, DateTime, SmallInteger, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from speakerflow_ai.models import SpeakingRequest


class SpeakingRequestBase(DeclarativeBase):
    pass


class SpeakingRequestModel(SpeakingRequestBase):
    __tablename__ = "speaking_requests"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    event_time: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    address: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    topic: Mapped[str] = mapped_column(String(), nullable=False)
    duration_in_minutes: Mapped[int] = mapped_column(SmallInteger(), nullable=False)
    requester_email: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)


def save(session: Session, speaking_request: SpeakingRequest) -> SpeakingRequest:
    speaking_request_model = SpeakingRequestModel(
        id=speaking_request.id,
        event_time=speaking_request.event_time,
        address=speaking_request.address.model_dump(mode="json"),
        topic=speaking_request.topic,
        duration_in_minutes=speaking_request.duration_in_minutes,
        requester_email=speaking_request.requester_email,
        status=speaking_request.status,
    )
    session.merge(speaking_request_model)
    session.commit()

    return speaking_request


def list_all(session: Session) -> list[SpeakingRequest]:
    records = session.scalars(select(SpeakingRequestModel)).all()

    return [
        SpeakingRequest(
            id=record.id,
            event_time=record.event_time,
            address=record.address,
            topic=record.topic,
            duration_in_minutes=record.duration_in_minutes,
            requester_email=record.requester_email,
            status=record.status,
        )
        for record in records
    ]


def get_by_id(session: Session, speaking_request_id: str) -> SpeakingRequest:
    record = session.scalar(
        select(SpeakingRequestModel).where(SpeakingRequestModel.id == speaking_request_id)
    )

    if record is None:
        raise ValueError(f"Speaking request with id '{speaking_request_id}' not found")

    return SpeakingRequest(
        id=record.id,
        event_time=record.event_time,
        address=record.address,
        topic=record.topic,
        duration_in_minutes=record.duration_in_minutes,
        requester_email=record.requester_email,
        status=record.status,
    )
