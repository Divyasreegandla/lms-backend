from fastapi import APIRouter,Depends
from fastapi_app.LMSauth.dependencies import get_current_user

router = APIRouter()

@router.get("/protected")
def protected(user=Depends(get_current_user)):
    return {"message": "Access granted", "user": user}