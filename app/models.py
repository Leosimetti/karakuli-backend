from pydantic import BaseModel, validator, Field, BaseConfig
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime
from pydantic import UUID4


class OID(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            return ObjectId(str(v))
        except InvalidId:
            raise ValueError("Not a valid ObjectId")


class MongoModel(BaseModel):
    class Config(BaseConfig):
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            ObjectId: lambda oid: str(oid),
        }

    @classmethod
    def from_mongo(cls, data: dict):
        """We must convert _id into "id". """
        if not data:
            return data
        id = data.pop('_id', None)
        return cls(**dict(data, id=id))

    def mongo(self, **kwargs):
        exclude_unset = kwargs.pop('exclude_unset', True)
        by_alias = kwargs.pop('by_alias', True)

        parsed = self.dict(
            exclude_unset=exclude_unset,
            by_alias=by_alias,
            **kwargs,
        )

        # Mongo uses `_id` as default key. We should stick to that as well.
        if '_id' not in parsed and 'id' in parsed:
            parsed['_id'] = parsed.pop('id')

        return parsed


class Review(MongoModel):
    # _id: UUID4
    word_id: OID = Field()
    srs_stage: int
    total_correct: int
    total_incorrect: int
    review_date: datetime

    # @validator("_id", pre=True, always=True)
    # def default_id(cls, v):
    #     return v or uuid.uuid4()


class ReviewSession(MongoModel):
    word_id: OID = Field()
    incorrect_answers: int


class BaseWord(MongoModel):
    grade: str
    writing: str
    readings: str
    meaning: str
    strokes: int
    user: UUID4

    # @validator("id", pre=True, always=True)
    # def default_id(cls, v):
    #     return v or uuid.uuid4()


class CreateWord(MongoModel):
    grade: str
    writing: str
    readings: str
    meaning: str
    strokes: int
