from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.utils.translation import ngettext
from core.models import MyDjangoQLSearchMixin
from users.models import JobDepartment, JobGroup, JobManagement, User, RefreshToken


@admin.register(User)
class MyUserAdmin(MyDjangoQLSearchMixin, UserAdmin):
    actions = ["shutdown_user"]
    search_fields = ("email", "first_name", "last_name", "middle_name")
    list_display = (
        "personnel_number",
        "email",
        "full_name",
        "job_title",
        "group",
        "date_joined"
    )
    ordering = ("date_joined",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
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
                    "personnel_number",
                    "job_title",
                    "group"
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
                    "personnel_number",
                    "job_title",
                    "group"
                )
            }
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser"
                ),
            },
        ),
    )

    def full_name(self, obj):
        return obj.__str__()

    def get_queryset(self, request):
        user = super(MyUserAdmin, self).get_queryset(request)
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


@admin.register(JobDepartment)
class JobDepartmentAdmin(MyDjangoQLSearchMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("title", "parent", "children", "is_deleted")}),
    )
    list_display = ("title", "parent", "children", "is_deleted")


@admin.register(JobGroup)
class JobGroup(MyDjangoQLSearchMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("title", "parent", "is_deleted")}),
    )
    list_display = ("title", "parent", "is_deleted")


@admin.register(JobManagement)
class JobManagementAdmin(MyDjangoQLSearchMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("title", "children", "is_deleted")}),
    )
    list_display = ("title", "children", "is_deleted")


@admin.register(ContentType)
class ContentTypeAdmin(admin.ModelAdmin):
    ...


@admin.register(Permission)
class PermissionaAdmin(admin.ModelAdmin):
    ...


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    ...


@admin.register(RefreshToken)
class RefreshTokenAdmin(MyDjangoQLSearchMixin, admin.ModelAdmin):
    readonly_fields = ("user", "refresh_token", "created_at")
