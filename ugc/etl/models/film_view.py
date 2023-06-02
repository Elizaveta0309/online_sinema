from datetime import datetime

from pydantic import BaseModel
from .base_model import ConfigMixin


class FilmView(BaseModel, ConfigMixin):
    user_id: str
    film_id: str
    viewed_frame: int
    created_at: datetime
