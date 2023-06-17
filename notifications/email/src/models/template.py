from uuid import UUID

from models.transform import OrjsonModel


class Template(OrjsonModel):
    """ Модель представления шаблона письма. """
    id: UUID
    name: str
    description: str
    subject: str
    template: str
