from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from core.models import MyDjangoQLSearchMixin
from users.models import User, JobDepartment, JobGroup, JobManagement


@admin.register(User)
class MyUserAdmin(MyDjangoQLSearchMixin, UserAdmin):
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
                    "groups"
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

    def get_queryset(self, request):
        user = super(MyUserAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return user
        return user.filter(id=request.user.id)


@admin.register(JobDepartment)
class JobDepartmentAdmin(MyDjangoQLSearchMixin, admin.ModelAdmin):
    list_display = ("title", "parent", "children", "is_delete")


@admin.register(JobGroup)
class JobGroup(MyDjangoQLSearchMixin, admin.ModelAdmin):
    ...


@admin.register(JobManagement)
class JobManagementAdmin(MyDjangoQLSearchMixin, admin.ModelAdmin):
    ...


@admin.register(ContentType)
class ContentTypeAdmin(admin.ModelAdmin):
    ...


@admin.register(Permission)
class PermissionaAdmin(admin.ModelAdmin):
    ...
