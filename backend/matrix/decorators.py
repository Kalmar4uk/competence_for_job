from django.shortcuts import render


def matrix_assignet_to(function):
    '''Декоратор для проверки назначения матрицы'''
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            return render(request, "matrix/error.html", status=403)
        return function(request)
    return wrapper
