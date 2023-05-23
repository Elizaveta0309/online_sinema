from fastapi import APIRouter, Depends, HTTPException, Request
from .query_params import TimeCodeParams
from src.services.time_code import TimeCodeService, get_time_code_service

router = APIRouter()


@router.post('/',
             description='Метод позволяет отправить информацию о номере последней просмотренной пользователем секунды',
             response_description='Time code of a film')
async def set_time_code(params: TimeCodeParams = Depends(), service: TimeCodeService = Depends(get_time_code_service)):
    return await service.set_time_code(params)
