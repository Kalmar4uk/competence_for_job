from api.models_for_api.base_model import ApiUser
from api.exceptions.error_422 import EmployeeInCompany
from django.shortcuts import get_object_or_404
from django.utils import timezone
from users.models import User
from companies.models import Company, OldCompanyEmployee
from django.http.response import Http404


def delete_employees_with_company(employee: int, company: Company) -> None:
    """Удаление сотрудника из компании"""
    employee_data = get_object_or_404(User, id=employee)
    employee_data.company = None
    employee_data.date_of_dismissal = timezone.now().date()
    employee_data.save()
    OldCompanyEmployee.objects.create(
        company=company,
        user=employee_data,
        job_title=employee_data.job_title,
        date_of_employment=employee_data.date_of_employment,
        date_of_dismissal=employee_data.date_of_dismissal,
    )


def added_employees_in_company(
    employees: list[int],
    company: Company
) -> list[ApiUser]:
    """Добавление сотрудников в компанию"""
    result: list[ApiUser] = []
    for employee in employees:
        try:
            employee_data = get_object_or_404(User, id=employee)
        except Http404:
            pass

        if employee_data.company:
            raise EmployeeInCompany()

        employee_data.company = company
        employee_data.date_of_employment = timezone.now().date()
        employee_data.date_of_dismissal = None
        employee_data.save()
        result.append(ApiUser.from_django_model(employee_data))

    return result
