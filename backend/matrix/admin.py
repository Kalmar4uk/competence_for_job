from core.models import MyDjangoQLSearchMixin
from django.contrib import admin, messages
from django.utils.translation import ngettext
from matrix.models import (GradeSkill, GradeSkillMatrix, Matrix, Skill,
                           TemplateMatrix)
from rangefilter.filters import DateRangeFilterBuilder


class MatrixSkillGradeWithTemplate(admin.TabularInline):
    model = GradeSkillMatrix
    readonly_fields = ("skills", "grades")
    extra = 0


@admin.register(Skill)
class SkillAdmin(MyDjangoQLSearchMixin, admin.ModelAdmin):
    list_display = ("id", "skill", "area_of_application")
    list_filter = ("area_of_application",)
    search_fields = ("skill",)
    readonly_fields = ("area_of_application",)


@admin.register(Matrix)
class MatrixAdmin(MyDjangoQLSearchMixin, admin.ModelAdmin):
    inlines = [MatrixSkillGradeWithTemplate]
    actions = ("change_status",)
    list_display = ("name", "user", "status", "created_at", "completed_at")
    list_filter = ("user",)
    search_fields = ("user",)
    readonly_fields = ("created_at",)

    @admin.action(description="Перевести в Завершено")
    def change_status(self, request, queryset):
        change_status_tasck = queryset.update(status="Завершена")
        for matrix in queryset:
            matrix.save()
        self.message_user(
            request,
            ngettext(
                ("%d Успешно изменен"),
                ("%d Успешно изменены"),
                change_status_tasck
            )
            % change_status_tasck,
            messages.SUCCESS
        )


@admin.register(GradeSkill)
class GardeSkillAdmin(admin.ModelAdmin):
    actions = None
    list_display = ("grade", "evaluation_number")
    readonly_fields = ("grade", "evaluation_number")

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(TemplateMatrix)
class TemplateMatrixAdmin(admin.ModelAdmin):
    filter_horizontal = ("skills",)
