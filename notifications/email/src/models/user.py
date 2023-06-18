from typing import Optional

from models.transform import OrjsonModel
from pydantic import EmailStr


class User(OrjsonModel):
    """ Модель представления пользователя. """
    email: Optional[EmailStr]
    login: Optional[str]
