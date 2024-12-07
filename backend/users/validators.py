from django.core.exceptions import ValidationError


def validation_min_length_personnal_number(data):
    if len(data) < 8:
        raise ValidationError(
            "Значение не может быть меньше 8"
        )
