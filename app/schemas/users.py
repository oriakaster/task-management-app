from pydantic import BaseModel, Field

# -------- Users --------
class UserCreate(BaseModel):
    username: str = Field(min_length=3)
    password: str = Field(min_length=4)

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

# -------- Authentication --------
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    username: str
    password: str
