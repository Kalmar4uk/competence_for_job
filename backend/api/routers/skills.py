from api.exceptions.error_404 import SkillNotFound
from api.exceptions.error_422 import SkillAlreadyExists
from api.models_for_api.base_model import ApiSkills
from api.models_for_api.model_request import ApiSkillsCreate
from api.models_for_api.models_response import ApiSkillsPaginator
from api.permissions import get_current_user
from api.routers.routers import router_skills
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from fastapi import Depends, Query
from matrix.models import Skill
from users.models import User


@router_skills.get("/", response_model=ApiSkillsPaginator)
def get_skills_list(
    page: int = Query(
        1,
        description="Номер страницы"
    ),
    limit: int = Query(
        30,
        description="Указать кол-во навыков если требуется"
    ),
    type: str | None = Query(
        None,
        description="Указать тип навыка (hard skill, soft skill или tool)"
    ),
    current_user: User = Depends(get_current_user)
):
    """Вывод всех навыков"""
    if type:
        skills_data = Skill.objects.filter(
            area_of_application=type.capitalize()
        )
    else:
        skills_data = Skill.objects.all()

    offset: int = (page - 1) * limit
    count: int = skills_data.count()
    skills = skills_data[offset:offset+limit]

    api_skills_list = [ApiSkills.from_django_model(skill) for skill in skills]

    next: int | None = page + 1 if offset + limit < count else None
    previous: int | None = page - 1 if page > 1 else None

    return ApiSkillsPaginator(
        count=count,
        next=next,
        previous=previous,
        result=api_skills_list
    )


@router_skills.get("/{skill_id}", response_model=ApiSkills)
def get_skill(
    skill_id: int,
    current_user: User = Depends(get_current_user)
):
    """Вывод навыка по id"""
    try:
        skill = get_object_or_404(Skill, id=skill_id)
    except Http404:
        raise SkillNotFound(skill_id=skill_id)

    return ApiSkills.from_django_model(skill)


@router_skills.post("/", response_model=ApiSkills)
def create_skill(
    from_data: ApiSkillsCreate,
    current_user: User = Depends(get_current_user)
):
    """Создание навыка"""
    if Skill.objects.filter(skill=from_data.skill).exists():
        raise SkillAlreadyExists(name=from_data.skill)

    new_skills = Skill.objects.create(
        area_of_application=from_data.area_of_application,
        skill=from_data.skill
    )
    return ApiSkills.from_django_model(new_skills)
