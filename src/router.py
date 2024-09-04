from fastapi import APIRouter
from src.schemes import Echo

router = APIRouter()

@router.get('/')
def hello() -> str:
    return {'Hello': 'World'}

@router.post('/echo/')
def echo(payload: Echo):
    return {'data': payload.stroka}

