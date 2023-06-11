from typing import Any, Optional

from models.transform import OrjsonModel
from pydantic import EmailStr


class NotificationEmail(OrjsonModel):

    email: Optional[EmailStr]
    content: Optional[Any]
