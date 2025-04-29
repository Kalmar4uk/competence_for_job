from api.exceptions.error_400 import NotValidStatusMatrix
from api.exceptions.error_404 import (MatrixNotFound,
                                      TemplateMatrixNotFound,
                                      UserNotFound)
from api.exceptions.error_422 import BadSkillInRequest, DoesNotMatchCountSkill
from api.models_for_api.model_request import (ApiMatrixCompeted,
                                              ApiMatrixCreate,
                                              ApiMatrixInWorkStatus
                                              )
from api.models_for_api.models_response import (
    ApiMatrixForResponse, ApiMatrixForResponseWithStatusAndLastUpdateFields,
)
from api.permissions import (check_matrix_user, get_current_user,
                             get_current_user_is_director_or_admin)
from api.routers.routers import router_matrix
from api.routers.utils import result_matrix_list, result_matrix
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from fastapi import Depends
from matrix.models import (GradeSkillMatrix,
                           Matrix,
                           Skill,
                           TemplateMatrix,
                           GradeSkill)
from users.models import User


@router_matrix.get(
        "/by_company",
        response_model=list[ApiMatrixForResponse],
        responses={401: {}, 403: {}})
def get_matrix_list_by_company(
    current_user: User = Depends(get_current_user_is_director_or_admin)
):
    """
    Выводит все матрицы сотрудников по компании директора
    который отправляет запрос
    """
    matrices = Matrix.objects.filter(user__company=current_user.company)
    return result_matrix_list(matrices=matrices)


@router_matrix.get(
        "/by_employee",
        response_model=list[ApiMatrixForResponse],
        responses={401: {}}
    )
def get_matrix_list_by_employee(
    current_user: User = Depends(get_current_user)
):
    """
    Выводит все матрицы сотрудника который отправляет запрос
    """
    matrices = Matrix.objects.filter(user=current_user)
    return result_matrix_list(matrices=matrices)


@router_matrix.post(
        "/",
        response_model=list[ApiMatrixForResponse],
        responses={401: {}, 403: {}, 404: {}})
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

    return result_matrix_list(matrices=matrices)


@router_matrix.put(
        "/{matrix_id}/new_status",
        response_model=ApiMatrixForResponseWithStatusAndLastUpdateFields,
        responses={401: {}, 403: {}, 404: {}, 422: {}}
    )
def in_work_status_matrix(
    matrix_id: int,
    from_data: ApiMatrixInWorkStatus,
    current_user: User = Depends(check_matrix_user)
):
    """Перевод матрицы в статус В процессе"""
    try:
        matrix = get_object_or_404(Matrix, id=matrix_id)
    except Http404:
        raise MatrixNotFound(matrix_id=matrix_id)

    if from_data.status == matrix.status:
        raise NotValidStatusMatrix()

    matrix.status = from_data.status
    matrix.last_update_status = timezone.now()
    matrix.save()

    return ApiMatrixForResponseWithStatusAndLastUpdateFields(
        status=matrix.status,
        last_update_status=matrix.last_update_status
    )


@router_matrix.patch(
        "/{matrix_id}/completed/",
        response_model=ApiMatrixForResponse,
        responses={401: {}, 403: {}, 404: {}, 422: {}}
    )
def completed_matrix(
    matrix_id: int,
    from_data: ApiMatrixCompeted,
    current_user: User = Depends(check_matrix_user)
):
    """перевод матрицы в завершенную"""
    try:
        matrix = get_object_or_404(Matrix, id=matrix_id)
    except Http404:
        raise MatrixNotFound(matrix_id=matrix_id)

    if from_data.status == matrix.status:
        raise NotValidStatusMatrix()

    skills_matrix = matrix.skills.values_list("skill", flat=True)

    original_count_skills: int = skills_matrix.count()

    if (
        original_count_skills > len(from_data.skills)
        or original_count_skills < len(from_data.skills)
    ):
        raise DoesNotMatchCountSkill()

    matrix_skills_grade: list = []

    for skill in from_data.skills:
        bad_skill: list = []
        if skill.skill not in skills_matrix:
            bad_skill.append(skill.skill)
        else:
            skills = Skill.objects.get(skill=skill.skill)
            grades = GradeSkill.objects.get(
                evaluation_number=skill.grade.evaluation_number
            )
            matrix_skills_grade.append(
                GradeSkillMatrix(
                    matrix=matrix,
                    skills=skills,
                    grades=grades
                )
            )
    if bad_skill:
        raise BadSkillInRequest(skills=bad_skill)

    GradeSkillMatrix.objects.filter(matrix=matrix).delete()
    GradeSkillMatrix.objects.bulk_create(matrix_skills_grade)

    matrix.name = from_data.name
    matrix.status = from_data.status
    matrix.completed_at = timezone.now()
    matrix.save()

    return result_matrix(matrix=matrix)
