from django.urls import path

from . import views

app_name = 'matrix'

urlpatterns = [
    path('', views.competence, name="matrix"),
    path('profile/<slug:personnel_number>/', views.profile, name="profile")

]
