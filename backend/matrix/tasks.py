from matrix.models import Competence, GradeSkill, Skill, User
from matrix.constants import CURRENT_MONTH
from celery import shared_task


@shared_task
def save_to_db(data, user_id):
    user = User.objects.get(id=user_id)
    Competence.objects.filter(
        user=user,
        created_at__month=CURRENT_MONTH
    ).delete()

    for skill, grade in data.items():
        new_skill = Skill.objects.get(skill=skill)
        grade_skill = GradeSkill.objects.get(grade=grade[0])
        Competence.objects.create(
            user=user,
            skill=new_skill,
            grade_skill=grade_skill
        )
