import enum
import uuid
from datetime import datetime

from pydantic import BaseModel


class Frequency(enum.Enum):

    once = 'once'
    daily = 'daily'
    weekly = 'weekly'
    monthly = 'monthly'


class Channel(enum.Enum):
    email = 'email'


class Priority(enum.Enum):

    low = 'low'
    high = 'high'


class AdminNotification(BaseModel):

    id: uuid.UUID
    user_group: str
    template_id: uuid.UUID
    subject: str
    channel: Channel
    frequency: Frequency
    priority: Priority
    next_planned_date: datetime
