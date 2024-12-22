from django.utils import timezone
from matrix.models import Competence, GradeSkill, Skill

CURRENT_DATE = timezone.now().date()


def save_to_db(data, user):
    for skill, grade in data.items():
        new_skill = Skill.objects.get(skill=skill)
        grade_skill = GradeSkill.objects.get(grade=grade[0])
        Competence.objects.create(
            user=user,
            skill=new_skill,
            grade_skill=grade_skill
        )
