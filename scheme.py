from pydantic import BaseModel

class UserOut(BaseModel):
    id: int
    name: str
    profile_picture: str

    class Config:
        orm_mode = True
