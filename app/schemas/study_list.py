from typing import Optional

from pydantic import BaseModel, constr, AnyUrl


class StudyListCreate(BaseModel):
    name: constr(regex=r"\D")
    description: str
    img_url: Optional[AnyUrl]
