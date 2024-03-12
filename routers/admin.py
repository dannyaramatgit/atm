from fastapi import APIRouter, status, HTTPException
from database.database import init_db

router = APIRouter(prefix="/admin")


@router.get("/init", status_code=status.HTTP_200_OK)
def init():
    try:
        return init_db()
    except:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="db already initialized")
