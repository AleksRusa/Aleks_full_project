import os
import sys
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import uvicorn
from fastapi import FastAPI
from sqlalchemy import text
from fastapi import Form, HTTPException, status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from database.database import async_session
from routers.todotasks import router as task_router
from routers.users import router as user_router
from database.models import User


app = FastAPI()
app.include_router(task_router)
app.include_router(user_router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    
    for error in errors:
        loc = error["loc"]
        msg = error["msg"]

        # Проверка на ошибку с email
        if "email" in loc:
            return JSONResponse(status_code=422, content={"message": "Некорректный email!"})

        # Проверка на ошибку с возрастом
        if "age" in loc:
            return JSONResponse(status_code=422, content={"message": "Возраст должен быть от 1 до 100 лет!"})

    return JSONResponse(status_code=422, content={"message": "Ошибка валидации данных", "details": errors})

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


    


if __name__ == "__main__":
    # asyncio.run(main())
    uvicorn.run(
        app="src.main:app",
        reload=True,
    )