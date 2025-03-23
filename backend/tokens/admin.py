from django.contrib import admin
from tokens.models import (BlackListAccessToken, BlackListRefreshToken,
                           RefreshToken)


@admin.register(RefreshToken)
class RefreshTokenAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at",)


@admin.register(BlackListRefreshToken)
class BlackListRefreshToken(admin.ModelAdmin):
    readonly_fields = ("revoked_at",)


@admin.register(BlackListAccessToken)
class BlackListAccessAdmin(admin.ModelAdmin):
    pass
