from matrix.models import Competence
from matrix.constants import CURRENT_DATE


def check_passing_date(user):
    return Competence.objects.filter(
            user=user,
            created_at__date=CURRENT_DATE
        )
