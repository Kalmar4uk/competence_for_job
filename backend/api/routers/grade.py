from api.models_for_api.base_model import ApiGrades
from api.permissions import get_current_user
from api.routers.routers import router_grades
from fastapi import Depends
from matrix.models import GradeSkill
from users.models import User


@router_grades.get("/", response_model=list[ApiGrades])
def get_grades(
    current_user: User = Depends(get_current_user)
):
    """Вывод всех оценок"""
    grades = GradeSkill.objects.all()
    return [ApiGrades.from_django_model(grade) for grade in grades]
