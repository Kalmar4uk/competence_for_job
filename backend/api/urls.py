from django.urls import include, path
from rest_framework import routers
from .views import SkillViewSet, GradeCompetenceJobTitleViewSet


app_name = 'api'
v1_router = routers.DefaultRouter()
v1_router.register("skills", SkillViewSet, basename="skills")
v1_router.register("grade-competence-job-title", GradeCompetenceJobTitleViewSet, basename="grade-competence")
# v1_router.register("competence", CompetenceViewSet, basename="competence")

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
