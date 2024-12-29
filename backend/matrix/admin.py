from django.contrib import admin
from core.models import MyDjangoQLSearchMixin
from matrix.models import (
    Skill, GradeSkill, GradeCompetenceJobTitle, Competence
)


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


@admin.register(Competence)
class CompetenceAdmin(MyDjangoQLSearchMixin, admin.ModelAdmin):
    list_display = ("user", "skill", "grade_skill", "created_at")
    readonly_fields = ("created_at",)


@admin.register(GradeSkill)
class GardeSkillAdmin(MyDjangoQLSearchMixin, admin.ModelAdmin):
    readonly_fields = ("grade", "evaluation_number")
