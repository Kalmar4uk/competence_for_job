from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, render

from matrix.constants import CURRENT_DATE, CURRENT_MONTH, save_to_db
from matrix.models import Competence, GradeCompetenceJobTitle, GradeSkill, User


@login_required
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
    personal_competence = Competence.objects.filter(
        user=user,
        created_at__month=current_month
    )
    personal_competence_grade = personal_competence.exclude(
        grade_skill__evaluation_number=0
    ).values(
        "skill__skill",
        "grade_skill__evaluation_number",
        "grade_skill__grade"
    )
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
        "competence_with_grade_zero": competence_with_grade_zero,
        "personal_competence_grade": personal_competence_grade,
        "general_sum_grade": general_sum_grade,
        "personal_sum_grade": personal_sum_grade
    }
    return render(request, "matrix/profile.html", context, status=200)
