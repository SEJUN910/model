# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import time
import math
from model_class import ModelClass


app = FastAPI()
# 모든 도메인에서 오는 요청을 허용하기 위한 CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 메소드 허 q용
    allow_headers=["*"],  # 모든 헤더 허용
)

class Keyword(BaseModel):
    keyword: str
    model: int

@app.post("/get-keyword/")
async def getKey(data: Keyword):
    start_time = time.time()
    
    keyword = data.keyword
    model = data.model

    init = ModelClass(keyword, model)
    answer = init.getKeyword()
    
    end_time = time.time()
    total_time = end_time - start_time

    gemini = False
    if model == 4:
        gemini = True
        
    return { 'result': answer, 'time': total_time, 'gemini': gemini }

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)