from fastapi import (
    APIRouter,
    Depends,
    Response,
    Request,
    HTTPException,
)
from fastapi.responses import RedirectResponse 
from sqlalchemy.ext.asyncio import AsyncSession
import httpx


router = APIRouter(prefix="/api", tags=["auth"])

@router.post("/vk-auth/callback/")
async def vk_callback(request: Request):
    code = request.query_params.get('code')
    state = request.query_params.get('state')
    device_id = request.query_params.get('device_id')
    code_verifier = request.query_params.get('code_verifier')
    print(code_verifier)

    if not code or not state or not device_id or not code_verifier:
        raise HTTPException(status_code=400, detail="Missing required parameters")
    # Остальная логика остаётся прежней
    async with httpx.AsyncClient() as client:
        vk_response = await client.post(
            "https://id.vk.com/oauth2/auth",
            data={
                "grant_type": "authorization_code",
                "code_verifier": code_verifier,
                "redirect_uri": "http://localhost",
                "code": code,
                "client_id": 53252724,
                "device_id": device_id,
                "state": state
            }
        )
    print(vk_response.json())
    print(vk_response.json())
    print(vk_response.json())
    
    # Проверяем ответ от VK API
    if vk_response.status_code != 200:
        raise HTTPException(status_code=vk_response.status_code, detail="VK API error")
    
    return vk_response.json()

