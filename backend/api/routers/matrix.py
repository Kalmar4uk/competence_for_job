from api.routers.routers import router_matrix
from api.models_for_api.models_response import ApiMatrixForResponse, ApiSkillsAndGradesForMatrix
from matrix.models import Matrix, GradeSkillMatrix, Skill
from users.models import User
from fastapi import Depends, Query
from api.permissions import (get_current_user,
                             get_current_user_is_director_or_admin)
from api.exceptions.error_400 import NotValidStatusMatrix
from api.exceptions.error_403 import NotRights
from api.exceptions.error_404 import (CompanyNotFound,
                                      UserNotFound,
                                      TemplateMatrixNotFound,
                                      MatrixNotFound)
from api.models_for_api.base_model import ApiCompany, ApiSkills, ApiUser, ApiGrades, ApiTemplateMatrix
from api.models_for_api.model_request import ApiTemplateMatrixUpdateOrCreate, ApiMatrixCreate, ApiMatrixInWorkStatus
from api.models_for_api.models_response import (ApiTemplateMatrixBaseGet,
                                                ApiTemplateMatrixPaginator)
from api.permissions import (check_matrix_user_or_not,
                             get_current_user,
                             get_current_user_is_director_or_admin)
from api.routers.utils import result_matrix, check_matrix_and_user
from companies.models import Company
from django.db.models import QuerySet
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from fastapi import Depends, Query
from matrix.constants import STATUSES_MATRIX
from matrix.models import TemplateMatrix, GradeSkillMatrix
from users.models import User


@router_matrix.get("/by_company", response_model=list[ApiMatrixForResponse])
def get_matrix_list_by_company(
    current_user: User = Depends(get_current_user_is_director_or_admin)
):
    """
    Выводит все матрицы сотрудников по компании директора
    который отправляет запрос
    """
    matrices = Matrix.objects.filter(user__company=current_user.company)
    return result_matrix(matrices=matrices)


@router_matrix.get("/by_employee", response_model=list[ApiMatrixForResponse])
def get_matrix_list_by_employee(
    current_user: User = Depends(get_current_user)
):
    """
    Выводит все матрицы сотрудника который отправляет запрос
    """
    matrices = Matrix.objects.filter(user=current_user)
    return result_matrix(matrices=matrices)


@router_matrix.post("/", response_model=list[ApiMatrixForResponse])
def create_matrix(
    from_data: ApiMatrixCreate,
    current_user: User = Depends(get_current_user_is_director_or_admin)
):
    """Создание матриц(-ы)"""
    try:
        template_matrix = get_object_or_404(
            TemplateMatrix,
            id=from_data.template_matrix
        )
    except Http404:
        raise TemplateMatrixNotFound(
            template_id=from_data.template_matrix
        )

    employees = User.objects.filter(id__in=from_data.employee)
    if not employees:
        raise UserNotFound(user_id=from_data.employee)

    skills = template_matrix.skills.all()
    matrices: list[Matrix] = []

    for employee in employees:
        matrix = Matrix.objects.create(
            name=from_data.name,
            template_matrix=template_matrix,
            user=employee
        )
        matrix.skills.set(skills)
        matrices.append(matrix)

    return result_matrix(matrices=matrices)


@router_matrix.put("/{matrix_id}/new_status", status_code=204)
def in_work_status_matrix(
    matrix_id: int,
    from_data: ApiMatrixInWorkStatus,
    current_user: User = Depends(check_matrix_user_or_not)
):
    """Перевод матрицы в статус В процессе"""
    matrix = current_user.matrix.get(id=matrix_id)

    status = from_data.status.capitalize()

    if status == matrix.status:
        raise NotValidStatusMatrix()
    if status not in STATUSES_MATRIX:
        raise NotValidStatusMatrix(status=status)

    matrix.status = from_data.status
    matrix.save()

    return {}


@router_matrix.patch("/{matrix_id}/completed/")
def completed_matrix(
    matrix_id: int,
    current_user: User = Depends(check_matrix_user_or_not)
):
    pass
