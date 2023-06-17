from fastapi import APIRouter, Depends

from src.services.notifications import NotificationsService, get_notifications_service
from .params import NewFilmParams

router = APIRouter()

@router.post('/',
             description='Метод позволяет позволяет положить в очередь событие  о новом фильме на платформе',
             response_description='Monthly notifications')
async def send_notifications(
    params: NewFilmParams= Depends(),
    service: NotificationsService = Depends(get_notifications_service)
):
    return await service.send_notification(params)
