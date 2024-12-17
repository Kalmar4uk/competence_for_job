from django.urls import include, path
from . import views

app_name = 'matrix'

urlpatterns = [
    path('', views.competence, name="matrix"),
    path('profile/<int:pk>/', views.profile, name="profile")

]
