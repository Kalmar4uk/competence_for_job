from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from dateutil.relativedelta import relativedelta

from matrix.constants import CURRENT_MONTH, CURRENT_DATE
from matrix.functions import check_passing_date, check_connect_redis
from matrix.models import Competence, GradeCompetenceJobTitle, GradeSkill, User
from matrix.tasks import download_file, save_to_db


@login_required
def for_main_page(request):
    users_same_group = User.objects.filter(
        group=request.user.group
        ).exclude(
            id=request.user.id
            )
    competence = Competence.objects.filter(
        user__in=users_same_group,
        created_at__month=CURRENT_MONTH
        ).values(
            "user__first_name",
            "user__last_name",
            "user__personnel_number"
            ).annotate(
                sum_grade=Sum("grade_skill__evaluation_number")
                )
    context = {
        "competence": competence
    }
    return render(request, "matrix/main_page.html", context)


@login_required
def matrix(request):
    user = request.user
    if check_passing_date(user):
        return render(request, "matrix/double.html")
    skills = GradeCompetenceJobTitle.objects.filter(
        job_title=user.job_title
    ).values(
        "skill__skill",
        "skill__area_of_application"
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
        if check_connect_redis():
            save_to_db.delay(data, user.id)
        else:
            save_to_db(data, user.id)
        return JsonResponse({
            "personnel_number": user.personnel_number
        }, status=201)
    return render(request, "matrix/matrix.html", context)


@login_required
def profile(request, personnel_number):
    current_date = CURRENT_DATE.replace(day=1)
    user_for_profile = get_object_or_404(
        User,
        personnel_number=personnel_number
    )
    personal_competence = Competence.objects.filter(
        user=user_for_profile,
        created_at__month=CURRENT_MONTH
    )
    personal_competence_grade = personal_competence.exclude(
        grade_skill__evaluation_number=0
    ).values(
        "skill__skill",
        "grade_skill__grade"
        ).order_by(
            "grade_skill__evaluation_number"
            )
    competence_with_grade_zero = personal_competence.filter(
        grade_skill__evaluation_number=0
    ).values(
        "skill__skill"
        )
    personal_sum_grade = personal_competence_grade.aggregate(
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
    old_personal_competence = Competence.objects.filter(
        user=user_for_profile,
        created_at__date__range=(
            current_date - relativedelta(months=3),
            (current_date - relativedelta(months=1))+relativedelta(day=31)
        )
    ).values("created_at").annotate(
        sum_grade=Sum("grade_skill__evaluation_number", default=0)
    ).order_by("-created_at")
    context = {
        "user_for_profile": user_for_profile,
        "old_personal_competence": old_personal_competence,
        "check_passing": check_passing_date(user_for_profile),
        "competence_with_grade_zero": competence_with_grade_zero,
        "personal_competence_grade": personal_competence_grade,
        "general_sum_grade": general_sum_grade,
        "personal_sum_grade": personal_sum_grade
    }
    return render(request, "matrix/profile.html", context)


@login_required
def competence_file(request, personnel_number):
    if check_connect_redis():
        stream = download_file.delay(personnel_number).get()
    else:
        stream = download_file(personnel_number)
    response = HttpResponse(
        content=stream,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": 'attachment; filename="competence.xlsx"'
        },
    )
    return response
