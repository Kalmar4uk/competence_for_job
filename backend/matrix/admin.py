from django.contrib import admin
from core.models import MyDjangoQLSearchMixin
from matrix.models import Skill, GradeCompetenceJobTitle, Competence, SkillCompetence


class SkillCompetenceInlines(admin.StackedInline):
    model = SkillCompetence
    extra = 0
    min_num = 1
    readonly_fields = ("date",)


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


@admin.register(Competence)
class CompetenceAdmin(MyDjangoQLSearchMixin, admin.ModelAdmin):
    list_display = ("user", "get_skills")
    inlines = (SkillCompetenceInlines,)

    @admin.display(description="Навык(-и)")
    def get_skills(self, obj):
        return ", ".join([skill.skill for skill in obj.skill.all()])


@admin.register(SkillCompetence)
class SkillCompetenceAdmin(MyDjangoQLSearchMixin, admin.ModelAdmin):
    readonly_fields = ("date",)
