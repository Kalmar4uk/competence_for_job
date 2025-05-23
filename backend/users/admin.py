from admin_auto_filters.filters import AutocompleteFilter
from core.models import MyDjangoQLSearchMixin
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext
from users.models import User


class CompanyFilter(AutocompleteFilter):
    title = "Компания"
    field_name = "company"


@admin.register(User)
class MyUserAdmin(MyDjangoQLSearchMixin, UserAdmin):
    actions = ["shutdown_user"]
    search_fields = ("email", "first_name", "last_name", "middle_name")
    list_display = (
        "email",
        "full_name",
        "job_title",
        "company",
        "date_joined"
    )
    list_filter = ("is_active", CompanyFilter)
    ordering = ("-date_joined",)
    raw_id_fields = ("company",)
    fieldsets = (
        (None, {"fields": (
            "email",
            "password",
            "first_name",
            "last_name",
            "middle_name"
        )}),
        (
            _("Сотрудник"),
            {
                "fields": (
                    "job_title",
                    "company",
                    'date_of_employment',
                    'date_of_dismissal',
                )
            }
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups"
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {"fields": ("email", "password1", "password2")}),
        (_("Personal info"), {
            "fields": (
                "first_name", "last_name", "middle_name"
            )
        }
        ),
        (
            _("Сотрудник"),
            {
                "fields": (
                    "job_title",
                )
            }
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups"
                ),
            },
        ),
    )

    def full_name(self, obj):
        return obj.__str__()

    def get_queryset(self, request):
        user = super().get_queryset(request)
        if request.user.is_superuser:
            return user
        return user.filter(id=request.user.id)

    @admin.action(description="Деактивировать сотрудников")
    def shutdown_user(self, request, queryset):
        deactivate_user = queryset.update(is_active=False)
        for user in queryset:
            user.save()
        self.message_user(
            request,
            ngettext(
                ("%d Успешно деактивирован"),
                ("%d Успешно деактивированы"),
                deactivate_user
            )
            % deactivate_user,
            messages.SUCCESS
        )


@admin.register(ContentType)
class ContentTypeAdmin(admin.ModelAdmin):
    ...


@admin.register(Permission)
class PermissionaAdmin(admin.ModelAdmin):
    ...


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    ...
