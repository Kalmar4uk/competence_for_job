from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from matrix.models import Skill, Competence, GradeSkill, User


def server_error(request):
    return render(request, "matrix/error.html", status=500)


def page_not_found(request, exception):
    return render(request, "matrix/error.html", status=404)


def csrf_permission_denied(request, reason=''):
    return render(request, "matrix/error.html", status=403)


# @login_required
def competence(request):
    skills = Skill.objects.all()
    skills_hard = skills.filter(area_of_application="Hard skill")
    skills_soft = skills.filter(area_of_application="Soft skill")
    skills_tool = skills.filter(area_of_application="Tool")
    grade_skills = GradeSkill.objects.all()
    context = {
        "skills_hard": skills_hard,
        "skills_soft": skills_soft,
        "skills_tool": skills_tool,
        "grade_skills": grade_skills
    }
    if request.POST:
        user = get_object_or_404(User, id=request.user.id)
        current_date = timezone.now().date()
        if Competence.objects.filter(user=user, date__date=current_date):
            return render(request, "matrix/double.html")
        data = dict(request.POST)
        data.pop("csrfmiddlewaretoken")
        save_to_db(data)
        return render(request, "matrix/succesfull.html")
    return render(request, "matrix/matrix.html", context)


def save_to_db(data):
    user = User.objects.get(id=1)
    for skill, grade in data.items():
        new_skill = Skill.objects.get(skill=skill)
        grade_skill = GradeSkill.objects.get(grade=grade[0])
        Competence.objects.create(
            user=user,
            skill=new_skill,
            grade_skill=grade_skill
        )


@login_required
def profile(request, personnel_number):
    user = get_object_or_404(User, personnel_number=personnel_number)
    context = {"user": user}
    return render(request, "matrix/profile.html", context)
