from api.routers.routers import router_matrix
from api.models_for_api.models_response import ApiMatrixForResponse, ApiSkillsAndGradesForMatrix
from matrix.models import Matrix, GradeSkillMatrix, Skill
from users.models import User
from fastapi import Depends, Query
from api.permissions import (get_current_user,
                             get_current_user_is_director_or_admin)
from api.exceptions.error_403 import NotRights
from api.exceptions.error_404 import (CompanyNotFound,
                                      UserNotFound,
                                      TemplateMatrixNotFound)
from api.models_for_api.base_model import ApiCompany, ApiSkills, ApiUser, ApiGrades, ApiTemplateMatrix
from api.models_for_api.model_request import ApiTemplateMatrixUpdateOrCreate, ApiMatrixCreate
from api.models_for_api.models_response import (ApiTemplateMatrixBaseGet,
                                                ApiTemplateMatrixPaginator)
from api.permissions import (get_current_user,
                             get_current_user_is_director_or_admin)
from api.routers.utils import result_matrix
from companies.models import Company
from django.db.models import QuerySet
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from fastapi import Depends, Query
from matrix.models import TemplateMatrix
from users.models import User


@router_matrix.get("/by_company", response_model=list[ApiMatrixForResponse])
def get_matrix_list_by_company(
    current_user: User = Depends(get_current_user_is_director_or_admin)
):
    matrices = Matrix.objects.filter(user__company=current_user.company)
    return result_matrix(matrices=matrices)


@router_matrix.get("/by_employee", response_model=list[ApiMatrixForResponse])
def get_matrix_list_by_employee(
    current_user: User = Depends(get_current_user)
):
    matrices = Matrix.objects.filter(user=current_user)
    return result_matrix(matrices=matrices)


@router_matrix.post("/", response_model=list[ApiMatrixForResponse])
def create_matrix(
    from_data: ApiMatrixCreate,
    current_user: User = Depends(get_current_user_is_director_or_admin)
):
    try:
        template_matrix = get_object_or_404(
            TemplateMatrix,
            id=from_data.template_matrix
        )
    except Http404:
        raise TemplateMatrixNotFound(
            template_id=from_data.template_matrix
        )
# дописать эндпоинт
