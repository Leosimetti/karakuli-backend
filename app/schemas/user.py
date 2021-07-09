from pydantic import BaseModel, EmailStr, constr


class UserBase(BaseModel):
    email: EmailStr
    username: constr(regex=r'^[0-9a-zA-Z_\-.]{5,64}$')

    def __str__(self):
        return f"{self.username} with {self.email}"


class UserCreate(UserBase):
    password: constr(regex=r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,64}$')


class UserGeneralResponse(UserBase):
    id: int
    verified: bool

    class Config:
        orm_mode = True
