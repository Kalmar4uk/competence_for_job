from api.models_for_api.base_model import ApiGradeSkill, ApiSkills, ApiUser, ApiMatrix
from api.models_for_api.model_request import ApiMatrixCreate
from api.models_for_api.models_response import (ApiMatrixCreateResponse,
                                                ApiMatrixWithGrade,
                                                ApiMatrixListSkills,
                                                ApiSkillsGradeMatrixResponse,
                                                ApiMatrixSkillsGrade)
from django.contrib.auth import get_user_model
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from fastapi import APIRouter, HTTPException, status, Depends
from matrix.models import Competence, GradeSkill, Skill, Matrix
from users.models import User
from api.auth import get_current_user


router_matrix = APIRouter(prefix="/matrix", tags=["matrix"])
router_skills = APIRouter(prefix="/skills", tags=["skills"])
router_grade = APIRouter(prefix="/grade", tags=["grade"])


@router_matrix.get("/", response_model=ApiMatrix)
def matrix_for_passing(
    current_user: User = Depends(get_current_user)
):
    user = ApiUser.from_django_model(current_user)
    matrix_data = Matrix.objects.get(user=current_user, status="Новая")
    skills_data = Skill.objects.filter(skill_competence__matrix=matrix_data)
    skills_list = []
    for skill in skills_data:
        skills_list.append(ApiSkills.from_django_model(skill))
    matrix = ApiMatrix.from_django_model(
        matrix=matrix_data,
        user=user,
        skills=skills_list
    )
    return matrix


@router_matrix.patch("/{matrix_id}", response_model=ApiMatrixWithGrade)
def matrix_for_passing_update(
    matrix_id: int,
    matrix_obj: ApiMatrixCreate,
    current_user: User = Depends(get_current_user),
):
    matrix_data = get_object_or_404(Matrix, id=matrix_id)
    if matrix_data.user != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Матрица не соответствует сотруднику"
        )
    user = ApiUser.from_django_model(current_user)
    skills_grade_list = []
    for matrix in matrix_obj.matrix:
        skill_data = get_object_or_404(Skill, skill=matrix.skill)
        grade_data = get_object_or_404(GradeSkill, grade=matrix.grade.grade)
        Competence.objects.filter(
            matrix=matrix_data,
            skill=skill_data
        ).update(
            grade_skill=grade_data
        )
        api_grade = ApiGradeSkill.from_django_model(grade_data)
        api_skill = ApiMatrixSkillsGrade(
            id=skill_data.id,
            area_of_application=skill_data.area_of_application,
            skill=skill_data.skill,
            grade=api_grade
        )
        skills_grade_list.append(api_skill)
    api_matrix = ApiMatrixWithGrade.from_django_model(
        matrix=matrix_data,
        user=user,
        skills=skills_grade_list
    )
    return api_matrix


@router_skills.get("/", response_model=list[ApiSkills])
def skills_list(area_of_application: str | None = None):
    basic_area_of_application = list(
        Skill.objects.values_list("area_of_application", flat=True).distinct()
    )
    if (
        area_of_application and
        area_of_application.capitalize() in basic_area_of_application
    ):
        skills_data = Skill.objects.filter(
            area_of_application=area_of_application.capitalize()
        )
        return [ApiSkills.from_django_model(skill) for skill in skills_data]
    skills_data = Skill.objects.all()
    return [ApiSkills.from_django_model(skill) for skill in skills_data]


@router_skills.get("/{skill_id}", response_model=ApiSkills)
def one_skill(skill_id: int):
    try:
        skill = get_object_or_404(Skill, id=skill_id)
        return ApiSkills.from_django_model(skill)
    except Http404 as e:
        raise HTTPException(
            status_code=404, detail=f"{str(e)}({str(skill_id)})"
        )


@router_grade.get("/", response_model=list[ApiGradeSkill])
def grade_list():
    try:
        grade_data = GradeSkill.objects.all()
        return [ApiGradeSkill.from_django_model(grade) for grade in grade_data]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router_grade.get("/{grade_id}", response_model=ApiGradeSkill)
def one_grade(grade_id: int):
    try:
        grade = get_object_or_404(GradeSkill, id=grade_id)
        return ApiGradeSkill.from_django_model(grade)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
