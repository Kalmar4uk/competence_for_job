from rest_framework import viewsets
from matrix.models import Skill, GradeCompetenceJobTitle, Competence, User
from users.models import JobDepartment, JobGroup, JobManagement

from .serializers import SkillSerializer, GradeCompetenceJobtitleSerialier


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    http_method_names = ['get']


class GradeCompetenceJobTitleViewSet(viewsets.ModelViewSet):
    queryset = GradeCompetenceJobTitle.objects.all()
    serializer_class = GradeCompetenceJobtitleSerialier
    http_method_names = ['get']


# class CompetenceViewSet(viewsets.ModelViewSet):
#     queryset = Competence.objects.all()
#     serializer_class = CompetenceSerializer
