from django.shortcuts import render


def server_error(request):
    return render(request, "matrix/error.html", status=500)


def page_not_found(request, exception):
    return render(request, "matrix/error.html", status=404)


def csrf_permission_denied(request, reason=''):
    return render(request, "matrix/error.html", status=403)