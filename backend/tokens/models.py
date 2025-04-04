from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class RefreshToken(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    refresh_token = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Refresh Token"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        verbose_name = "Refresh Token"
        verbose_name_plural = "Refresh Tokens"

    def __str__(self):
        return self.refresh_token


class BlackListRefreshToken(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="black_refresh_tokens"
    )
    token = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Refresh Token"
    )
    revoked_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        verbose_name = "Отозванный refresh token"
        verbose_name_plural = "Отозванные refresh tokens"

    def __str__(self):
        return self.token


class BlackListAccessToken(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="black_access_tokens"
    )
    token = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Access Token"
    )

    def __str__(self):
        return self.token
