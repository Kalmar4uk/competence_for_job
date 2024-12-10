from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from core.models import MyDjangoQLSearchMixin
from users.models import User, JobDepartment, JobGroup, JobManagement


@admin.register(User)
class MyUserAdmin(MyDjangoQLSearchMixin, UserAdmin):
    search_fields = ("email", "first_name", "last_name", "middle_name")
    list_display = (
        "email",
        "full_name",
        "job_title",
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
                    "group",
                    "department",
                    "management"
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
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None, {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'password1',
                    'password2',
                    'first_name',
                    'last_name',
                    'is_superuser',
                    'is_staff',
                    'is_active'
                )
            }
        ),
    )

    def full_name(self, obj):
        if obj.middle_name:
            return f"{obj.first_name} {obj.last_name} {obj.middle_name}"
        return f"{obj.first_name} {obj.last_name}"


@admin.register(JobDepartment)
class JobDepartmentAdmin(MyDjangoQLSearchMixin, admin.ModelAdmin):
    ...


@admin.register(JobGroup)
class JobGroup(MyDjangoQLSearchMixin, admin.ModelAdmin):
    ...


@admin.register(JobManagement)
class JobManagementAdmin(MyDjangoQLSearchMixin, admin.ModelAdmin):
    ...
