from django.shortcuts import redirect
from matrix.constants import JOB_TITLE_USERS


# Оказывается я уже делал эту проверку,
# но в шаблоне и которая работает до сих пор.
# suka blyat'
# Оставлю, пусть будет.
def check_job_title_for_matrix(function):
    '''Декоратор для проверки должности челика'''
    def wrapper(request, *args, **kwargs):
        if request.user.job_title not in JOB_TITLE_USERS:
            return redirect("matrix:profile", request.user.personnel_number)
        return function(request)
    return wrapper
