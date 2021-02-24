from pydantic import BaseModel


class BaseSchema(BaseModel):
    pass

    class Config:
        orm_mode = True


class IdMixin(BaseModel):
    id: int


class TimestampMixin(BaseModel):
    created_at: int
    updated_at: int
