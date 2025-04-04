import os
from tempfile import NamedTemporaryFile

from celery import shared_task
from dateutil.relativedelta import relativedelta
from django.shortcuts import get_object_or_404
from matrix.constants import CURRENT_DATE, CURRENT_DATETIME, CURRENT_MONTH
from matrix.exceptions import NotNull
from matrix.models import Competence, GradeSkill, Matrix, Skill, User
from openpyxl import Workbook


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
    user = get_object_or_404(User, id=user_id)
    matrix = get_object_or_404(Matrix, user=user, status="Новая")
    competence = Competence.objects.filter(matrix=matrix)

    for comp in competence:
        for skill, grade in data.items():
            obj_grade_skill = GradeSkill.objects.get(grade=grade[0])
            if comp.skill.skill == skill:
                comp.grade_skill = obj_grade_skill
                comp.save()

    for check_none in competence:
        if check_none.grade_skill is None:
            raise NotNull(
                "Не все навыки оценены!"
            )
    matrix.status = "Завершена"
    matrix.completed_at = CURRENT_DATETIME
    matrix.save()


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
