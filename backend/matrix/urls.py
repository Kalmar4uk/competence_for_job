from django.urls import path

from . import views

app_name = 'matrix'

urlpatterns = [
    path("", views.for_main_page, name="main"),
    path("matrix/", views.matrix, name="matrix"),
    path("profile/<slug:personnel_number>/", views.new_profile, name="profile"),
    path(
        "competence_file/<slug:personnel_number>/<str:period>/",
        views.competence_file,
        name="competence_file"
    )
]
