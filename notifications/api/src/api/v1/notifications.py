from fastapi import APIRouter, Depends

#from src.services.time_code import TimeCodeService, get_time_code_service

from .params import LikeParams, NewFilmsParams, SomeEventParams

router = APIRouter()


@router.post('/',
             description='Метод позволяет положить в очередь уведомление о новом лайке на отзыве пользователя',
             response_description='Like notification')
async def send_like_notification(
    params: LikeParams = Depends(),
    #service: TimeCodeService = Depends(get_time_code_service)
):
    return await service.set_time_code(params)

@router.post('/',
             description='Метод позволяет позволяет положить в очередь событие о еженедельной рассылке о новых фильмах на платформе',
             response_description='Monthly notifications')
async def send_monthly_notifications(
    params: NewFilmsParams= Depends(),
    #service: TimeCodeService = Depends(get_time_code_service)
):
    return await service.set_time_code(params)

@router.post('/',
             description='Метод позволяет отправить положить в очередь событие о ручном уведомлении от менеджера',
             response_description='Notification by manager')
async def send_personalized_notification(
    params: SomeEventParams = Depends(),
    #service: TimeCodeService = Depends(get_time_code_service)
):
    return await service.set_time_code(params)