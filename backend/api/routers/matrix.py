from fastapi import APIRouter, HTTPException, status
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from matrix.models import Skill, GradeSkill, User
from api.models_for_api import ApiGradeSkill, ApiMatrixGet, ApiMatrixCreate, ApiSkills, ApiMatrixCreateResponse, ApiSkillsGradeMatrixResponse, ApiUser

router_matrix = APIRouter(prefix="/matrix", tags=["matrix"])
router_skills = APIRouter(prefix="/skills", tags=["skills"])


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
            skill = ApiSkills(
                **model_to_dict(
                    get_object_or_404(
                        Skill,
                        skill=mat.skills
                    )
                )
            )
            grade = ApiGradeSkill(
                **model_to_dict(
                    get_object_or_404(
                        GradeSkill,
                        grade=mat.grade
                    )
                )
            )
            response_list.append(ApiSkillsGradeMatrixResponse(
                skills=skill,
                grade=grade
                )
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return ApiMatrixCreateResponse(user=ApiUser(**user), matrix=response_list)


@router_skills.get("/", response_model=list[ApiSkills])
def skills_list():
    skills_data = Skill.objects.all().values()
    return [ApiSkills(**skill) for skill in skills_data]


@router_skills.get("/{skill_id}", response_model=ApiSkills)
def read_one_skill(skill_id: int):
    try:
        skill = model_to_dict(get_object_or_404(Skill, id=skill_id))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return ApiSkills(**skill)
