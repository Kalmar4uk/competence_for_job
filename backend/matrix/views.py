from django.views.generic import ListView, CreateView
from django.shortcuts import render, redirect
from django.db.models import Q
from matrix.models import Skill, GradeCompetenceJobTitle, Competence, GradeSkill, User


def succesfull(request):
    return render(request, "matrix/succesfull.html")


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
        data = dict(request.POST)
        data.pop("csrfmiddlewaretoken")
        save_to_db(data)
        return redirect("matrix:succesfull")
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
