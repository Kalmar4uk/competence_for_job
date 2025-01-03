from django.urls import include, path
from rest_framework import routers

from .views import (CompetenceViewSet, GradeCompetenceJobTitleViewSet,
                    SkillViewSet, UserViewSet)

app_name = 'api'
v1_router = routers.DefaultRouter()
v1_router.register("users", UserViewSet, basename="users")
v1_router.register("skills", SkillViewSet, basename="skills")
v1_router.register(
    "grade-competence-job-title",
    GradeCompetenceJobTitleViewSet,
    basename="grade-competencies"
)
v1_router.register("Заупа", CompetenceViewSet, basename="competencies")

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
