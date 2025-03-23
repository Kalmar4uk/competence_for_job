import os
from celery import shared_task
from tempfile import NamedTemporaryFile
from openpyxl import Workbook
from django.db.models import F
from django.shortcuts import get_object_or_404
from dateutil.relativedelta import relativedelta

from matrix.models import Competence, GradeSkill, Skill, User, Matrix, GradeCompetenceJobTitle
from matrix.constants import CURRENT_MONTH, NAME_FOR_TASK_MATRIX, CURRENT_DATE


@shared_task
def generate_matrix_for_user():
    users = User.objects.filter(is_active=True)
    for user in users:
        matrix = Matrix.objects.create(user=user)
        skills = Skill.objects.filter(
            grade_competence__job_title=user.job_title
        ).exclude(
            grade_competence__min_grade__evaluation_number=0
        )
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
def download_file(personnel_number, period):
    user = User.objects.get(personnel_number=personnel_number)
    personal_matrix = Matrix.objects.filter(
        user=user
    ).order_by(
        "-created_at"
    ).prefetch_related(
        "competencies"
    )
    if period == "last" or period == "current_month":
        current_personel_matrix = personal_matrix.filter(
            created_at__month=CURRENT_MONTH
        )
        if period == "last":
            competencies = Competence.objects.filter(
                matrix=current_personel_matrix.filter(status="Завершена")[0]
            ).values_list(
                "skill__skill",
                "grade_skill__grade",
                "matrix__created_at__date"
            )
        else:
            competencies = Competence.objects.filter(
                matrix__in=current_personel_matrix.filter(status="Завершена")
            ).values_list(
                "skill__skill",
                "grade_skill__grade",
                "matrix__created_at__date"
            )
    else:
        current_date = CURRENT_DATE.replace(day=1)
        old_matrix = personal_matrix.filter(
            created_at__date__range=(
                current_date - relativedelta(months=3),
                (current_date - relativedelta(months=1))+relativedelta(day=31)
            )
        )
        competencies = Competence.objects.filter(
            matrix__in=old_matrix
        ).values_list(
            "skill__skill",
            "grade_skill__grade",
            "matrix__created_at__date"
        )

    wb = Workbook()
    sheet = wb.active
    sheet.title = 'competence'
    sheet.append(["Навык", "Оценка", "Дата"])
    for competence in competencies:
        sheet.append(competence)
    with NamedTemporaryFile(delete=False) as tmp:
        wb.save(tmp.name)
        tmp.seek(0)
        stream = tmp.read()
        tmp.close()
        os.unlink(tmp.name)
    return stream
