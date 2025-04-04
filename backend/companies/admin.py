from django.contrib import admin
from users.models import User

from .models import Company, LegalDetailsCompany


class UserInlines(admin.TabularInline):
    model = User
    fields = ("email", "job_title", "is_director")
    extra = 0


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    inlines = [UserInlines]
    list_display = ("name", "is_active", "created_at", "closed_at")
    readonly_fields = ("created_at",)


@admin.register(LegalDetailsCompany)
class LegalDetailsCompanyAdmin(admin.ModelAdmin):
    pass
