from django.urls import include, path
from . import views

app_name = 'matrix'

urlpatterns = [
    path('', views.competence, name="matrix"),
    path('profile/<int:personnel_number>/', views.profile, name="profile")

]
