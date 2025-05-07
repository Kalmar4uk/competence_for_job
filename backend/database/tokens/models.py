from database.core.models import BaseModel, CreatedAtMixin
from tortoise import fields


class RefreshToken(BaseModel, CreatedAtMixin):
    user = fields.ForeignKeyField(
        model_name="models.User",
        on_delete=fields.CASCADE,
        related_name="refresh_tokens"
    )
    refresh_token = fields.CharField(max_length=255, unique=True)
    expires_at = fields.DatetimeField()

    class Meta:
        table = "refreshtoken"


class BlackListRefreshToken(RefreshToken):
    user = fields.ForeignKeyField(
        model_name="models.User",
        on_delete=fields.CASCADE,
        related_name="black_refresh_tokens"
    )

    class Meta:
        table = "blacklistrefreshtoken"


class BlackListAccessToken(BaseModel):
    user = fields.ForeignKeyField(
        model_name="models.User",
        on_delete=fields.CASCADE,
        related_name="black_access_token"
    )
    access_token = fields.CharField(max_length=255, unique=True)

    class Meta:
        table = "blacklistaccesstoken"
