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
from starlette.middleware.sessions import SessionMiddleware

from routers.todotasks import router as task_router
from routers.users import router as user_router
from routers.auth import router as auth_router


app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key="odfljfdsgfdvdfmvdfl;mvlae",
    session_cookie="session_cookie"
)

app.include_router(task_router)
app.include_router(user_router)
app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost", "http://172.20.10.2:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(
        app="src.main:app",
        reload=True,
    )
