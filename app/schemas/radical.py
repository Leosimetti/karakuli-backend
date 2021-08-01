from pydantic import BaseModel


# Todo change str to constr with proper validation
class RadicalCreate(BaseModel):
    radical: str
    meaning: str
    strokes: int
