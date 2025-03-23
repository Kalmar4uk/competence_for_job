from django.forms.models import model_to_dict
from pydantic import BaseModel


class ApiBaseModelIfFieldsMatch(BaseModel):

    @classmethod
    def from_django_model(cls, model):
        data = model_to_dict(model)
        return cls(**data)


class ApiUserFromDjangoModel(BaseModel):

    @classmethod
    def from_django_model(cls, model):
        return cls(
            id=model.id,
            email=model.email,
            personnel_number=model.personnel_number,
            first_name=model.first_name,
            last_name=model.last_name,
            job_title=model.job_title
        )
