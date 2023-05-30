from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Like(BaseModel):
    user_id: str
    film_id: str
    date_time: Optional[datetime] = None
