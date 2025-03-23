from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from dateutil.relativedelta import relativedelta

from matrix.constants import CURRENT_MONTH, CURRENT_DATE
from matrix.functions import check_connect_redis
from matrix.models import Competence, GradeCompetenceJobTitle, GradeSkill, Matrix, User
from matrix.tasks import download_file, save_to_db


@login_required
def for_main_page(request):
    users_same_group = User.objects.filter(
        group=request.user.group
        ).exclude(
            id=request.user.id
            )
    matrix = Matrix.objects.filter(
        user__in=users_same_group,
        created_at__month=CURRENT_MONTH,
        status="Завершена"
    ).values(
        "user__first_name",
        "user__last_name",
        "user__personnel_number"
        ).annotate(
            sum_grade=Sum("competencies__grade_skill__evaluation_number")
        )
    context = {
        "matrix": matrix
    }

    return render(request, "matrix/main_page.html", context)


@login_required
def matrix(request):
    user = request.user

    skills = GradeCompetenceJobTitle.objects.filter(
        job_title=user.job_title
    ).values(
        "skill__skill",
        "skill__area_of_application",
        "min_grade__grade"
        ).exclude(
            min_grade__evaluation_number=0
            ).order_by("skill__skill")
    grade_skills = GradeSkill.objects.values("grade")
    for_cycle = [1, 2, 3]

    context = {
        "range": for_cycle,
        "skills": skills,
        "grade_skills": grade_skills
    }

    if request.POST:
        data = dict(request.POST)
        data.pop("csrfmiddlewaretoken")
        if not data:
            return HttpResponse(status=404)

        try:
            if check_connect_redis():
                save_to_db.delay(data, user.id)
            else:
                save_to_db(data, user.id)

            return JsonResponse({
                "personnel_number": user.personnel_number
            }, status=201)

        except Exception as e:
            return JsonResponse({"except": str(e)}, status=400)

    return render(request, "matrix/matrix.html", context)


@login_required
def competence_file(request, personnel_number, period):
    if check_connect_redis():
        stream = download_file.delay(personnel_number, period).get()
    else:
        stream = download_file(personnel_number, period)
    response = HttpResponse(
        content=stream,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": 'attachment; filename="competence.xlsx"'
        },
    )
    return response


@login_required
def new_profile(request, personnel_number):
    current_date = CURRENT_DATE.replace(day=1)
    user_for_profile = get_object_or_404(
        User,
        personnel_number=personnel_number
    )
    personal_matrix = Matrix.objects.filter(
        user=user_for_profile,
        created_at__month=CURRENT_MONTH
    ).order_by(
        "-created_at"
    ).prefetch_related(
        "competencies"
    )
    not_completed_personal_matrix = personal_matrix.filter(status="Новая")
    last_completed_personal_matrix = personal_matrix.filter(status="Завершена")[0]
    last_competence = Competence.objects.filter(
        matrix=last_completed_personal_matrix
    ).values(
        "skill__skill",
        "grade_skill__grade"
    )
    competence_for_current_month = Competence.objects.filter(
        matrix__in=personal_matrix
    ).values(
        "skill__skill",
        "grade_skill__grade"
    )
    last_personal_sum_grade = last_competence.aggregate(
        sum_grade=Sum(
            "grade_skill__evaluation_number", default=0
        )
    )["sum_grade"]
    current_month_sum_grade = competence_for_current_month.aggregate(
        sum_grade=Sum(
            "grade_skill__evaluation_number", default=0
        )
    )["sum_grade"]
    general_sum_grade = GradeCompetenceJobTitle.objects.filter(
        Q(job_title=user_for_profile.job_title) &
        ~Q(min_grade__evaluation_number=0)
    ).aggregate(
        sum_grade=Sum("min_grade__evaluation_number", default=0)
    )["sum_grade"]
    old_personal_matrix = Matrix.objects.filter(
        user=user_for_profile,
        created_at__date__range=(
            current_date - relativedelta(months=3),
            (current_date - relativedelta(months=1))+relativedelta(day=31)
        )
    ).order_by(
        "-created_at"
    ).prefetch_related(
        "competencies"
    )
    old_personal_competence = Competence.objects.filter(
        matrix__in=old_personal_matrix
        ).values("matrix__created_at", "matrix__status").annotate(
            sum_grade=Sum("grade_skill__evaluation_number", default=0)
        ).order_by("-matrix__created_at")

    context = {
        "user_for_profile": user_for_profile,
        "not_completed_personal_matrix": not_completed_personal_matrix,
        "last_competence": last_competence,
        "competence_for_current_month": competence_for_current_month,
        "last_personal_sum_grade": last_personal_sum_grade,
        "current_month_sum_grade": current_month_sum_grade,
        "general_sum_grade": general_sum_grade,
        "old_personal_competence": old_personal_competence
    }

    return render(request, "matrix/new_profile.html", context)
