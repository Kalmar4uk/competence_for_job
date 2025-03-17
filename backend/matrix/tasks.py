import os
from celery import shared_task
from tempfile import NamedTemporaryFile
from openpyxl import Workbook
from django.shortcuts import get_object_or_404

from matrix.models import Competence, GradeSkill, Skill, User, Matrix
from matrix.constants import CURRENT_MONTH, NAME_FOR_TASK_MATRIX


@shared_task
def generate_matrix_for_user():
    users = User.objects.filter(is_active=True)
    skills = Skill.objects.all()
    for user in users:
        matrix = Matrix.objects.create(user=user)
        for skill in skills:
            Competence.objects.create(skill=skill, matrix=matrix)


@shared_task
def save_to_db(data, user_id):
    pass
    # user = User.objects.get(id=user_id)
    # Competence.objects.filter(
    #     user=user,
    #     created_at__month=CURRENT_MONTH
    # ).delete()

    # for skill, grade in data.items():
    #     new_skill = get_object_or_404(Skill, skill=skill)
    #     grade_skill = get_object_or_404(GradeSkill, grade=grade[0])
    #     Competence.objects.create(
    #         user=user,
    #         skill=new_skill,
    #         grade_skill=grade_skill
    #     )


@shared_task
def download_file(personnel_number):
    pass
    # user = User.objects.get(personnel_number=personnel_number)
    # competencies = Competence.objects.filter(
    #     user=user
    # ).values_list(
    #     "skill__skill",
    #     "grade_skill__grade",
    #     "created_at__date"
    # )
    # wb = Workbook()
    # sheet = wb.active
    # sheet.title = 'competence'
    # sheet.append(["Навык", "Оценка", "Дата"])
    # for competence in competencies:
    #     sheet.append(competence)
    # with NamedTemporaryFile(delete=False) as tmp:
    #     wb.save(tmp.name)
    #     tmp.seek(0)
    #     stream = tmp.read()
    #     tmp.close()
    #     os.unlink(tmp.name)
    # return stream
