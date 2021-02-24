from pasteme.schemas.base import BaseSchema, IdMixin, TimestampMixin


class RecordOut(BaseSchema, IdMixin, TimestampMixin):
    content: str
    type: str
