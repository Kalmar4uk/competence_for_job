from django.db.models import Q, Avg
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from matrix.constants import CURRENT_DATE, save_to_db
from matrix.decorators import matrix_assignet_to
from matrix.models import Skill, Competence, GradeSkill, User


@matrix_assignet_to
def competence(request):
    skills = Skill.objects.values("area_of_application", "skill")
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
        user = get_object_or_404(User, id=request.user.id)
        current_date = CURRENT_DATE
        if Competence.objects.filter(user=user, created_at__date=current_date):
            return render(request, "matrix/double.html")
        save_to_db(data, user)
        return render(request, "matrix/succesfull.html")
    return render(request, "matrix/matrix.html", context)


@login_required
def profile(request, personnel_number):
    user = get_object_or_404(User, personnel_number=personnel_number)
    competence = Competence.objects.filter(user=user)
    competence_avg = competence.aggregate(
        Avg(
            "grade_skill__evaluation_number"
        )
    )["grade_skill__evaluation_number__avg"]
    context = {
        "user": user,
        "competence_avg": competence_avg,
        "competence": competence}
    return render(request, "matrix/profile.html", context)
