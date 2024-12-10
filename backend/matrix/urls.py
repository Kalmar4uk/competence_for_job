from django.urls import include, path
from . import views

app_name = 'matrix'

urlpatterns = [
    path('', views.competence, name="create"),
    path('succesfull/', views.succesfull, name="succesfull")
]
