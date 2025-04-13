from django.contrib import admin
from core.models import MyDjangoQLSearchMixin
from users.models import User
from rangefilter.filters import DateRangeFilterBuilder

from .models import Company, LegalDetailsCompany, OldCompanyEmployee


class UserInlines(admin.TabularInline):
    model = User
    fields = ("email", "job_title")
    extra = 0

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.exclude(groups__id=1)
        return queryset


@admin.register(Company)
class CompanyAdmin(MyDjangoQLSearchMixin, admin.ModelAdmin):
    inlines = [UserInlines]
    search_fields = ("name",)
    list_display = ("name", "is_active", "created_at", "closed_at")
    list_filter = (
        "is_active",
        ("created_at", DateRangeFilterBuilder()),
        ("closed_at", DateRangeFilterBuilder())
    )
    readonly_fields = ("created_at",)


@admin.register(LegalDetailsCompany)
class LegalDetailsCompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(OldCompanyEmployee)
class OldCompanyEmployeeAdmin(MyDjangoQLSearchMixin, admin.ModelAdmin):
    search_fields = ("company", "user")
    list_display = (
        "user",
        "company",
        "date_of_employment",
        "date_of_dismissal"
    )
    list_filter = (
        "user",
        "company",
        ("date_of_employment", DateRangeFilterBuilder()),
        ("date_of_dismissal", DateRangeFilterBuilder())
    )
