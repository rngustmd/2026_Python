# 라우터
from fastapi import APIRouter

router = APIRouter( prefix="/api" )

# 예측 요청
# http://127.0.0.1:8000/api/predict
from Service import apt_service
@router.post("/predict")
async def save( apt:dict ) :
    return apt_service.predict(apt)