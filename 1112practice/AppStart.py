# AppStart.py : FastAPI 실행 파일
# Controller.py : HTTP REST 파일
# Service.py : 로직(모델 예측) 파일
# 실행 위치 : 2026_Python 폴더에서 이 파일 실행 (1112practice\AppStart.py) ( 오른쪽 클릭 -> run python )
from fastapi import FastAPI
import uvicorn
app = FastAPI()

# [수업 외 추가] CORS 허용 : index.html(브라우저) 에서 axios 로 서버 호출 가능하게 함
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware( CORSMiddleware , allow_origins=["*"] ,
                    allow_methods=["*"] , allow_headers=["*"] )

# 컨트롤러에 라우터 연결
import Controller
app.include_router( Controller.router )

# 서버 실행 , 확인 : http://127.0.0.1:8000/docs
if __name__ == "__main__" :
    uvicorn.run( app , host="127.0.0.1" , port=8000 )
