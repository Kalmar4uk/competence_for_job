from celery import shared_task
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.utils import timezone
from matrix.models import Matrix

User = get_user_model()


@shared_task
def change_matrix_status_to_expired():
    matrices = Matrix.objects.filter(
        Q(deadline__lt=timezone.now()) &
        (~Q(status="Завершена") | ~Q(status="Просрочена"))
    )
    matrices.update(status="Просрочена")
