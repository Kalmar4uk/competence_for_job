from django.contrib import admin
from .models import Company, LegalDetailsCompany
from users.models import User

class UserInlines(admin.TabularInline):
    model = User
    fields = ("email", "job_title", "is_director")
    extra = 0


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    inlines = [UserInlines]
    readonly_fields = ("created_at", "closed_at")


@admin.register(LegalDetailsCompany)
class LegalDetailsCompanyAdmin(admin.ModelAdmin):
    pass
