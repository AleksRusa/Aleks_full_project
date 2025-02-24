import os
import sys
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import uvicorn
from fastapi import FastAPI
from sqlalchemy import text

from database.database import async_session
from routers.todotasks import router
from database.models import Users


app = FastAPI()
app.include_router(router)

    


if __name__ == "__main__":
    # asyncio.run(main())
    uvicorn.run(
        app="src.main:app",
        reload=True,
    )