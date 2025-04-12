from django.contrib import admin
from users.models import User

from .models import Company, LegalDetailsCompany, OldCompanyEmployee


class UserInlines(admin.TabularInline):
    model = User
    fields = ("email", "job_title", "is_director")
    extra = 0

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.exclude(is_director=True)
        return queryset


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    inlines = [UserInlines]
    list_display = ("name", "is_active", "created_at", "closed_at")
    readonly_fields = ("created_at",)


@admin.register(LegalDetailsCompany)
class LegalDetailsCompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(OldCompanyEmployee)
class OldCompanyEmployeeAdmin(admin.ModelAdmin):
    pass
