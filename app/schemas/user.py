from pydantic import BaseModel, EmailStr, constr

import inspect
from typing import Type

from fastapi import Form
from pydantic import BaseModel
from pydantic.fields import ModelField


def as_form(cls: Type[BaseModel]):
    new_parameters = []

    for field_name, model_field in cls.__fields__.items():
        model_field: ModelField  # type: ignore

        if not model_field.required:
            new_parameters.append(
                inspect.Parameter(
                    model_field.alias,
                    inspect.Parameter.POSITIONAL_ONLY,
                    default=Form(model_field.default),
                    annotation=model_field.outer_type_,
                )
            )
        else:
            new_parameters.append(
                inspect.Parameter(
                    model_field.alias,
                    inspect.Parameter.POSITIONAL_ONLY,
                    default=Form(...),
                    annotation=model_field.outer_type_,
                )
            )

    async def as_form_func(**data):
        return cls(**data)

    sig = inspect.signature(as_form_func)
    sig = sig.replace(parameters=new_parameters)
    as_form_func.__signature__ = sig  # type: ignore
    setattr(cls, 'as_form', as_form_func)
    return cls


class UserBase(BaseModel):
    email: EmailStr
    username: str  # constr(regex=r'^[0-9a-zA-Z_\-.]{5,64}$') # Todo @todo add later

    def __str__(self):
        return f"{self.username} with {self.email}"

@as_form
class UserCreate(UserBase):
    password: str  # constr(regex=r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,64}$')  # Todo @todo add later


class UserGeneralResponse(UserBase):
    id: int
    verified: bool

    class Config:
        orm_mode = True
