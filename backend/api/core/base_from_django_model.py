from django.forms.models import model_to_dict
from pydantic import BaseModel


class ApiBaseModelIfFieldsMatch(BaseModel):

    @classmethod
    def from_django_model(cls, model):
        data = model_to_dict(model)
        return cls(**data)


class ApiUserFromDjangoModel(BaseModel):

    @classmethod
    def from_django_model(cls, model, company=None):
        if company:
            return cls(
                id=model.id,
                email=model.email,
                first_name=model.first_name,
                last_name=model.last_name,
                job_title=model.job_title,
                role=model.groups.first.name if model.groups.all() else None,
                company=company
            )
        return cls(
            id=model.id,
            email=model.email,
            first_name=model.first_name,
            last_name=model.last_name,
            job_title=model.job_title
        )


class ApiCompanyFromDjangoModel(BaseModel):

    @classmethod
    def from_django_model(cls, model, director=None, employees=None):
        if not director:
            return cls(
                id=model.id,
                name=model.name,
                is_active=model.is_active
            )
        return cls(
            id=model.id,
            name=model.name,
            is_active=model.is_active,
            director=director,
            employees=employees,
            created_at=model.created_at,
            closed_at=model.closed_at
        )


class ApiTemplateMatrixFromDjangoModel(BaseModel):

    @classmethod
    def from_django_model(cls, model, author=None, company=None, skills=None):
        return cls(
            id=model.id,
            name=model.name,
            created_at=model.created_at,
            author=author,
            company=company,
            skills=skills
        )
