from fastapi import APIRouter, HTTPException, status
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from matrix.models import Skill, GradeSkill, User, Competence
from api.models_for_api import ApiGradeSkill, ApiMatrixGet, ApiMatrixCreate, ApiSkills, ApiMatrixCreateResponse, ApiSkillsGradeMatrixResponse, ApiUser

router_matrix = APIRouter(prefix="/matrix", tags=["matrix"])
router_skills = APIRouter(prefix="/skills", tags=["skills"])
router_grade = APIRouter(prefix="/grade", tags=["grade"])


@router_matrix.get("/", response_model=ApiMatrixGet)
def matrix_list():
    skills_data = Skill.objects.all().values()
    grade_data = GradeSkill.objects.all().values()
    skills = [ApiSkills(**skill) for skill in skills_data]
    grades = [ApiGradeSkill(**grade) for grade in grade_data]
    return ApiMatrixGet(skills=skills, grade=grades)


@router_matrix.post(
        "/",
        response_model=ApiMatrixCreateResponse,
        status_code=status.HTTP_201_CREATED
    )
def matrix_create(matrix: ApiMatrixCreate):
    response_list = []
    try:
        user = get_object_or_404(User, id=matrix.user)
        for mat in matrix.matrix:
            skill = get_object_or_404(Skill, skill=mat.skills)
            grade = get_object_or_404(GradeSkill, grade=mat.grade)
            competence = Competence.objects.create(
                user=user,
                skill=skill,
                grade_skill=grade
            )
            skill_response = ApiSkills(**model_to_dict(skill))
            grade_response = ApiGradeSkill(**model_to_dict(grade))
            response_list.append(ApiSkillsGradeMatrixResponse(
                skills=skill_response,
                grade=grade_response,
                created_at=competence.created_at
                )
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
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
def skills_list():
    skills_data = Skill.objects.all().values()
    return [ApiSkills(**skill) for skill in skills_data]


@router_skills.get("/{skill_id}", response_model=ApiSkills)
def one_skill(skill_id: int):
    try:
        skill = model_to_dict(get_object_or_404(Skill, id=skill_id))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return ApiSkills(**skill)


@router_grade.get("/", response_model=list[ApiGradeSkill])
def grade_list():
    grade_data = GradeSkill.objects.all().values()
    return [ApiGradeSkill(**grade) for grade in grade_data]


@router_grade.get("/{grade_id}", response_model=ApiGradeSkill)
def one_grade(grade_id: int):
    try:
        grade = model_to_dict(get_object_or_404(GradeSkill, id=grade_id))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return ApiGradeSkill(**grade)
