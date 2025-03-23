from core.models import MyDjangoQLSearchMixin
from django.contrib import admin, messages
from django.utils.translation import ngettext
from matrix.models import (Competence, GradeCompetenceJobTitle, GradeSkill,
                           Matrix, Skill)
from rangefilter.filters import DateRangeFilterBuilder


class CompetenceInline(admin.TabularInline):
    model = Competence
    extra = 1


@admin.register(Skill)
class SkillAdmin(MyDjangoQLSearchMixin, admin.ModelAdmin):
    list_display = ("id", "skill", "area_of_application")
    list_filter = ("area_of_application",)
    search_fields = ("skill",)
    readonly_fields = ("area_of_application",)


@admin.register(GradeCompetenceJobTitle)
class GradeCompetenceJobTitleAdmin(MyDjangoQLSearchMixin, admin.ModelAdmin):
    list_display = ("id", "job_title", "skill", "min_grade")
    list_filter = ("job_title", "min_grade", "skill")
    search_fields = ("skill", "job_title")
    readonly_fields = ("job_title", "skill", "min_grade")


@admin.register(Matrix)
class MatrixAdmin(MyDjangoQLSearchMixin, admin.ModelAdmin):
    actions = ("change_status",)
    inlines = (CompetenceInline,)
    list_display = ("name", "user", "status", "created_at", "completed_at")
    list_filter = ("user",)
    search_fields = ("user",)
    readonly_fields = ("created_at", "completed_at")

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
