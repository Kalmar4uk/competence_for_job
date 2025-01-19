from django.urls import path

from . import views

app_name = 'matrix'

urlpatterns = [
    path("", views.for_main_page, name="main"),
    path("matrix/", views.matrix, name="matrix"),
    path("profile/<slug:personnel_number>/", views.profile, name="profile"),
    path(
        "competence_file/<slug:personnel_number>/",
        views.competence_file,
        name="competence_file"
    )
]
