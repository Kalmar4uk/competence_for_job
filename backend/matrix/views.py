from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from matrix.constants import CURRENT_MONTH
from matrix.functions import check_passing_date, save_to_db
from matrix.models import Competence, GradeCompetenceJobTitle, GradeSkill, User


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
                sum_grade=Sum(
                    "grade_skill__evaluation_number"
                    )
                )
    context = {
        "competence": competence
    }
    return render(request, "matrix/main_page.html", context)


@login_required
def matrix(request):
    user = request.user
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
    if check_passing_date(user):
        return render(request, "matrix/double.html")
    if request.POST:
        data = dict(request.POST)
        data.pop("csrfmiddlewaretoken")
        save_to_db(data, request.user)
        return HttpResponse(status=201)
    return render(request, "matrix/matrix.html", context)


@login_required
def profile(request, personnel_number):
    user = get_object_or_404(User, personnel_number=personnel_number)
    personal_competence = Competence.objects.filter(
        user=user,
        created_at__month=CURRENT_MONTH
    )
    personal_competence_grade = personal_competence.exclude(
        grade_skill__evaluation_number=0
    ).values(
        "skill__skill",
        "grade_skill__grade"
    ).order_by("grade_skill__evaluation_number")
    competence_with_grade_zero = personal_competence.filter(
        grade_skill__evaluation_number=0
    ).values("skill__skill")
    personal_sum_grade = personal_competence_grade.aggregate(
        sum_grade=Sum(
            "grade_skill__evaluation_number"
        )
    )["sum_grade"]
    general_sum_grade = GradeCompetenceJobTitle.objects.filter(
        Q(job_title=user.job_title) & ~Q(min_grade__evaluation_number=0)
    ).aggregate(
        sum_grade=Sum(
            "min_grade__evaluation_number"
            )
        )["sum_grade"]
    context = {
        "user": user,
        "check_passing": check_passing_date(user),
        "competence_with_grade_zero": competence_with_grade_zero,
        "personal_competence_grade": personal_competence_grade,
        "general_sum_grade": general_sum_grade,
        "personal_sum_grade": personal_sum_grade
    }
    return render(request, "matrix/profile.html", context)
