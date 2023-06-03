from fastapi import APIRouter, Depends

from ugc.src.api.permission import check_permission
from ugc.src.services.time_code import TimeCodeService, get_time_code_service

from .params_for_query import TimeCodeParams

router = APIRouter()


@router.post('/',
             description='Метод позволяет отправить информацию о номере последней просмотренной пользователем секунды',
             response_description='Time code of a film')
@check_permission(required_role=['admin', 'subscriber'])
async def set_time_code(
    params: TimeCodeParams = Depends(),
    service: TimeCodeService = Depends(get_time_code_service)
):
    return await service.set_time_code(params)
