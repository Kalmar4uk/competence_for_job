from django.contrib import admin
from rangefilter.filters import DateRangeFilterBuilder

from core.models import MyDjangoQLSearchMixin
from matrix.models import (Matrix, Competence, GradeCompetenceJobTitle, GradeSkill,
                           Skill)


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
    inlines = (CompetenceInline,)
    list_display = ("name", "user", "created_at", "completed_at")
    list_filter = ("user",)
    search_fields = ("user",)
    readonly_fields = ("created_at", "completed_at")


@admin.register(GradeSkill)
class GardeSkillAdmin(admin.ModelAdmin):
    actions = None
    list_display = ("grade", "evaluation_number")
    readonly_fields = ("grade", "evaluation_number")

    def has_delete_permission(self, request, obj=None):
        return False
