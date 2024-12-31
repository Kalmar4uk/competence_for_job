from rest_framework import viewsets

from matrix.models import Competence, GradeCompetenceJobTitle, Skill, User
from users.models import JobDepartment, JobGroup, JobManagement

from .serializers import (CompetenceSerializer,
                          GradeCompetenceJobtitleSerialier,
                          SkillForJobSerializer, UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get']


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillForJobSerializer
    http_method_names = ['get']


class GradeCompetenceJobTitleViewSet(viewsets.ModelViewSet):
    queryset = GradeCompetenceJobTitle.objects.all()
    serializer_class = GradeCompetenceJobtitleSerialier
    http_method_names = ['get']


class CompetenceViewSet(viewsets.ModelViewSet):
    queryset = Competence.objects.all()
    serializer_class = CompetenceSerializer
    http_method_names = ['get']
