from pydantic import BaseModel
from django.forms.models import model_to_dict


class ApiBaseModelIfFieldsMatch(BaseModel):

    @classmethod
    def from_django_model(cls, model):
        data = model_to_dict(model)
        return cls(**data)
