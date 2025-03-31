from api.models_for_api import base_model
from django.forms.models import model_to_dict
from pydantic import BaseModel


class ApiBaseModelIfFieldsMatch(BaseModel):

    @classmethod
    def from_django_model(cls, model):
        data = model_to_dict(model)
        return cls(**data)


class ApiMatrixFromDjangoModel(BaseModel):

    @classmethod
    def from_django_model(cls, matrix, user, skills):
        return cls(
            id=matrix.id,
            name=matrix.name,
            user=user,
            status=matrix.status,
            skills=skills,
            created_at=matrix.created_at,
            completed_at=matrix.completed_at
        )


class ApiUserFromDjangoModel(BaseModel):

    @classmethod
    def from_django_model(cls, model):
        return cls(
            id=model.id,
            email=model.email,
            first_name=model.first_name,
            last_name=model.last_name,
            job_title=model.job_title
        )
