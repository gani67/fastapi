from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import SessionLocal
from .. import models, schemas
import shutil
import os

router = APIRouter()

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.post("/upload-profile-picture")
async def upload_profile_picture(name: str, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    file_location = f"static/{file.filename}"
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

    user = models.User(name=name, profile_picture=file_location)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {"message": "Profile picture uploaded", "user_id": user.id}

@router.get("/user/{user_id}", response_model=schemas.UserOut)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.get(models.User, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result
