from matrix.models import Competence, GradeSkill, Skill
from matrix.constants import CURRENT_DATE, CURRENT_MONTH


def save_to_db(data, user):
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


def check_passing_date(user):
    return Competence.objects.filter(
            user=user,
            created_at__date=CURRENT_DATE
        )
