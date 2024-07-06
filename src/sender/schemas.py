from datetime import datetime, timedelta
from typing import Self

from pydantic import BaseModel, model_validator


class SendMessageSchema(BaseModel):
    message: str
    minute: int
    hour: int
    day: int
    month: int
    year: int

    @model_validator(mode="after")
    def validate_date(self) -> Self:
        if self.year and self.month and self.day and self.hour and self.minute:

            scheduled_at = datetime(
                year=self.year,
                month=self.month,
                day=self.day,
                hour=self.hour,
                minute=self.minute,
            )

            if scheduled_at < datetime.now() + timedelta(minutes=1):
                raise ValueError(
                    "Date must be greater than the current one by at least a minute"
                )

        return self
