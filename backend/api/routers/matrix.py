from fastapi import APIRouter, HTTPException, status
from django.http.response import Http404
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from matrix.models import Skill, GradeSkill, User, Competence
from api.models_for_api.base_model import ApiGradeSkill, ApiSkills, ApiUser
from api.models_for_api.model_request import ApiMatrixCreate
from api.models_for_api.models_response import (
    ApiMatrixCreateResponse,
    ApiMatrixGet,
    ApiMatrixListSkillsAndGrade,
    ApiSkillsGradeMatrixResponse
)


router_matrix = APIRouter(prefix="/matrix", tags=["matrix"])
router_skills = APIRouter(prefix="/skills", tags=["skills"])
router_grade = APIRouter(prefix="/grade", tags=["grade"])


@router_matrix.get("/", response_model=ApiMatrixGet)
def matrix_list(area_of_application: str | None = None):
    skills_data = Skill.objects.all()
    grade_data = GradeSkill.objects.all()
    grades = [ApiGradeSkill.from_django_model(grade) for grade in grade_data]
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
    matrix = []
    for skill in skills_data:
        matrix.append(
            ApiMatrixListSkillsAndGrade(
                id=skill.id,
                area_of_application=skill.area_of_application,
                skill=skill.skill,
                grade=grades
            )
        )
    return ApiMatrixGet(matrix=matrix)


@router_matrix.post(
        "/",
        response_model=ApiMatrixCreateResponse,
        status_code=status.HTTP_201_CREATED
    )
def matrix_create(matrix: ApiMatrixCreate):
    response_list = []
    try:
        user = get_object_or_404(User, id=matrix.user)
    except Http404 as e:
        raise HTTPException(
            status_code=404, detail=str(e)
        )
    for mat in matrix.matrix:
        try:
            skill = get_object_or_404(Skill, skill=mat.skills)
            grade = get_object_or_404(GradeSkill, grade=mat.grade)
        except Http404 as e:
            raise HTTPException(
                status_code=404, detail=str(e)
            )
        try:
            competence = Competence.objects.create(
                user=user,
                skill=skill,
                grade_skill=grade
            )
            skill_response = ApiSkills.from_django_model(competence.skill)
            grade_response = ApiGradeSkill.from_django_model(
                competence.grade_skill
            )
            response_list.append(ApiSkillsGradeMatrixResponse(
                skills=skill_response,
                grade=grade_response,
                created_at=competence.created_at
                )
            )
        except Exception as e:
            HTTPException(
                status_code=400, detail=str(e)
            )
    user_response = ApiUser(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        job_title=user.job_title
    )
    return ApiMatrixCreateResponse(
        user=user_response,
        competence=response_list
    )


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
        grade = model_to_dict(get_object_or_404(GradeSkill, id=grade_id))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return ApiGradeSkill(**grade)
