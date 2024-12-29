from django.db.models import Sum
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from matrix.constants import CURRENT_DATE, CURRENT_MONTH, save_to_db
from matrix.models import (
    Competence, GradeSkill, GradeCompetenceJobTitle, User
)


def competence(request):
    skills = GradeCompetenceJobTitle.objects.filter(
        job_title=request.user.job_title
    ).values(
        "skill__skill",
        "skill__area_of_application"
        ).exclude(
            min_grade__evaluation_number=0
            )
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
        current_date = CURRENT_DATE
        if Competence.objects.filter(
            user=request.user,
            created_at__date=current_date
        ):
            return render(request, "matrix/double.html", status=204)
        save_to_db(data, request.user)
        return render(request, "matrix/succesfull.html", status=201)
    return render(request, "matrix/matrix.html", context, status=200)


@login_required
def profile(request, personnel_number):
    current_month = CURRENT_MONTH
    user = get_object_or_404(User, personnel_number=personnel_number)
    general_sum_grade = GradeCompetenceJobTitle.objects.filter(
        job_title=user.job_title
    ).exclude(min_grade__evaluation_number=0).aggregate(
        sum_grade=Sum("min_grade__evaluation_number")
    )["sum_grade"]
    competence_grade = Competence.objects.filter(
        user=user,
        created_at__month=current_month
    ).values("skill__skill", "grade_skill__evaluation_number")
    personal_sum_grade = competence_grade.aggregate(
        sum_grade=Sum("grade_skill__evaluation_number")
    )["sum_grade"]

    context = {
        "competence_grade": competence_grade,
        "general_sum_grade": general_sum_grade,
        "personal_sum_grade": personal_sum_grade
    }
    return render(request, "matrix/profile.html", context, status=200)
