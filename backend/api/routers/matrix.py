from api.exceptions.error_400 import NotValidStatusMatrix
from api.exceptions.error_404 import (MatrixNotFound, TemplateMatrixNotFound,
                                      UserNotFound)
from api.exceptions.error_422 import (BadSkillInRequest,
                                      DoesNotMatchCountSkill)
from api.models_for_api.model_request import (ApiMatrixCompeted,
                                              ApiMatrixCreate,
                                              ApiMatrixInWorkStatus,
                                              ApiMatrixRevision)
from api.models_for_api.models_response import (
    ApiMatrixForResponse,
    ApiMatrixForResponseWithStatusAndLastUpdateFields,
    ApiMatrixForResponseRevision,
    ApiMatrixPaginator
)
from api.permissions import (check_matrix_user, get_current_user,
                             get_current_user_is_director_or_admin)
from api.routers.routers import router_matrix
from api.routers.utils import result_matrix, result_matrix_list
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
from fastapi import Depends, Query
from matrix.models import (GradeSkill, GradeSkillMatrix, Matrix, Skill,
                           TemplateMatrix)
from matrix.constants import STATUSES_MATRIX
from users.models import User


@router_matrix.get(
        "/by_company",
        response_model=ApiMatrixPaginator,
        responses={401: {}, 403: {}})
def get_matrix_list_by_company(
    page: int = Query(
        1,
        description="Номер страницы"
    ),
    limit: int = Query(
        10,
        description="Указать кол-во матриц если требуется"
    ),
    employee: int | None = Query(
        None,
        description="Указать id сотрудника"
    ),
    status: str = Query(
        "all",
        description=(
            "Указать статус матриц (Новая, В процессе, Просрочена, Завершена)"
        )
    ),
    current_user: User = Depends(get_current_user_is_director_or_admin)
):
    """
    Выводит все матрицы сотрудников по компании директора
    который отправляет запрос
    """
    if employee:
        matrices = Matrix.objects.filter(
            Q(user__company=current_user.company) & Q(user=employee)
        )
    else:
        matrices = Matrix.objects.filter(user__company=current_user.company)

    if (form_state := status.capitalize()) in STATUSES_MATRIX:
        matrices = matrices.filter(status=form_state)

    offset: int = (page - 1) * limit

    count: int = matrices.count()
    matrices_data = matrices[offset:offset+limit]
    result_matrix = result_matrix_list(matrices=matrices_data)

    next: int | None = page + 1 if offset + limit < count else None
    previous: int | None = page - 1 if page > 1 else None

    return ApiMatrixPaginator(
        count=count,
        next=next,
        previous=previous,
        result=result_matrix
    )


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


@router_matrix.get("/{matrix_id}", response_model=ApiMatrixForResponse)
def get_matrix(matrix_id: int, current_user: User = Depends(get_current_user)):
    """Выводит матрицу по id"""
    try:
        matrix = get_object_or_404(Matrix, id=matrix_id)
    except Http404:
        raise MatrixNotFound(matrix_id=matrix_id)

    return result_matrix(matrix=matrix)


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
        matrix.deadline = from_data.deadline
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
    """Перевод матрицы в завершенную"""
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


@router_matrix.patch(
        "/{matrix_id}/revision",
        response_model=ApiMatrixForResponseRevision
    )
def revision_for_matrix(
    matrix_id: int,
    from_data: ApiMatrixRevision,
    current_user: User = Depends(get_current_user)
):
    """Возврат матрицы на доработку"""
    try:
        matrix = get_object_or_404(Matrix, id=matrix_id)
    except Http404:
        raise MatrixNotFound(matrix_id=matrix_id)

    matrix.status = "В процессе"
    matrix.last_update_status = timezone.now()
    matrix.completed_at = None
    matrix.deadline = timezone.now() + timedelta(days=5)
    base_matrix_for_respose = result_matrix(matrix=matrix)
    return ApiMatrixForResponseRevision(
        **base_matrix_for_respose.model_dump(),
        comment=from_data.comment
    )
