from fastapi import APIRouter, Depends, HTTPException, Request
from .query_params import TimeCodeParams
from src.services.time_code import TimeCodeService, get_time_code_service

router = APIRouter()


@router.post('/', description='Метод позволяет отправить информацию о просмотре фильма',
            response_description='Time code of a film')
async def time_code(params: TimeCodeParams = Depends(), service: TimeCodeService = Depends(get_time_code_service)):
    return await service.post_time_code(params)


