from django.contrib.auth.password_validation import validate_password
from django.db.models import Avg, Q
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from matrix.models import (Competence, GradeCompetenceJobTitle, GradeSkill,
                           Skill, User)
from users.models import JobDepartment, JobGroup, JobManagement


class UserSerializer(serializers.ModelSerializer):
    group = serializers.StringRelatedField()
    department = serializers.StringRelatedField()
    management = serializers.StringRelatedField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "middle_name",
            "job_title",
            "group",
            "department",
            "management"
        )


class GradeSkillSerializers(serializers.ModelSerializer):

    class Meta:
        model = GradeSkill
        fields = ("id", "grade", "evaluation_number")


class SkillForJobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = ("id", "skill", "area_of_application")
        read_only_fields = ("area_of_application",)


class GradeCompetenceJobtitleSerialier(serializers.ModelSerializer):
    skill = SkillForJobSerializer()
    min_grade = GradeSkillSerializers()

    class Meta:
        model = GradeCompetenceJobTitle
        fields = ("id", "job_title", "min_grade", "skill")


class CompetenceSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    skill = SkillForJobSerializer()
    grade_skill = GradeSkillSerializers()
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Competence
        fields = ("id", "user", "skill", "grade_skill", "created_at")
