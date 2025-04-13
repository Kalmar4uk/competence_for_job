# import os
# from tempfile import NamedTemporaryFile

# from celery import shared_task
# from dateutil.relativedelta import relativedelta
# from django.contrib.auth import get_user_model
# from django.shortcuts import get_object_or_404
# from matrix.constants import CURRENT_DATE, CURRENT_DATETIME, CURRENT_MONTH
# from matrix.exceptions import NotNull
# from matrix.models import Competence, GradeSkill, Matrix, Skill

# User = get_user_model()


# @shared_task
# def generate_matrix_for_user():
#     users = User.objects.filter(is_active=True)
#     for user in users:
#         matrix = Matrix.objects.create(user=user)
#         skills = Skill.objects.filter(
#             grade_competence__job_title=user.job_title
#         ).exclude(
#             grade_competence__min_grade__evaluation_number=0
#         )
#         for skill in skills:
#             Competence.objects.create(skill=skill, matrix=matrix)


# @shared_task
# def save_to_db(data, user_id):
#     user = get_object_or_404(User, id=user_id)
#     matrix = get_object_or_404(Matrix, user=user, status="Новая")
#     competence = Competence.objects.filter(matrix=matrix)

#     for comp in competence:
#         for skill, grade in data.items():
#             obj_grade_skill = GradeSkill.objects.get(grade=grade[0])
#             if comp.skill.skill == skill:
#                 comp.grade_skill = obj_grade_skill
#                 comp.save()

#     for check_none in competence:
#         if check_none.grade_skill is None:
#             raise NotNull(
#                 "Не все навыки оценены!"
#             )
#     matrix.status = "Завершена"
#     matrix.completed_at = CURRENT_DATETIME
#     matrix.save()
