from fastapi import APIRouter, Depends


from src.services.time_code import TimeCodeService, get_time_code_service

from .params_for_query import TimeCodeParams
from typing import Any

from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.services.auth_service import Auth

router = APIRouter()
bearer_token = HTTPBearer()
auth = Auth()




@router.post('/',
             description='Метод позволяет отправить информацию о номере последней просмотренной пользователем секунды',
             response_description='Time code of a film')
async def set_time_code(
    params: TimeCodeParams = Depends(),
    service: TimeCodeService = Depends(get_time_code_service),
    request: HTTPAuthorizationCredentials = Depends(bearer_token),
):
    token = request.credentials
    user_id = auth.decode_token(token)
    return await service.set_time_code(params, user_id)

# from fastapi import APIRouter, Depends

# from src.api.permission import check_permission
# from src.services.time_code import TimeCodeService, get_time_code_service

# from .params_for_query import TimeCodeParams

# router = APIRouter()


# @router.post('/',
#              description='Метод позволяет отправить информацию о номере последней просмотренной пользователем секунды',
#              response_description='Time code of a film')
# @check_permission(required_role=['admin', 'subscriber'])
# async def set_time_code(
#     params: TimeCodeParams = Depends(),
#     service: TimeCodeService = Depends(get_time_code_service)
# ):
#     return await service.set_time_code(params)
