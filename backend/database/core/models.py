from tortoise.models import Model
from tortoise import fields


class BaseModel(Model):
    id = fields.IntField(primary_key=True)

    class Meta:
        abstract = True


class CreatedAtMixin():
    created_at = fields.DatetimeField(auto_now_add=True)
