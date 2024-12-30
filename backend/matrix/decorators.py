import logging

from django.shortcuts import render


def matrix_assignet_to(function):
    '''Декоратор для проверки назначения матрицы'''
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            response = render(request, "matrix/error.html", status=403)
            logging.error(
                f"method: {request.method}, "
                f"path: {request.path}, "
                f"user_id: {request.user.id}, "
                f"user_email: {request.user.email}, "
                f"status_code: {response.status_code}, "
                f"error: {response.reason_phrase}"
            )
            return response
        return function(request)
    return wrapper
