from django.contrib.auth.password_validation import validate_password
from django.db.models import Avg, Q
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from matrix.models import Skill, GradeCompetenceJobTitle, Competence, User
from users.models import JobDepartment, JobGroup, JobManagement


class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = ("id", "skill", "area_of_application")
        read_only_fields = ("area_of_application",)


class GradeCompetenceJobtitleSerialier(serializers.ModelSerializer):
    skill = SkillSerializer()

    class Meta:
        model = GradeCompetenceJobTitle
        fields = ("id", "job_title", "min_grade", "skill")


# class CompetenceSerializer(serializers.ModelSerializer):
#     skill = SkillSerializer()

#     class Meta:
#         model = Competence
#         fields = ("id", "user", "skill", "grade_skill", "date")
