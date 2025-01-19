from django.db import models
from djangoql.admin import DjangoQLSearchMixin


class MyDjangoQLSearchMixin(DjangoQLSearchMixin):
    djangoql_completion_enabled_by_default = False


class GeneralHierarchy(models.Model):
    title = models.CharField("Название", max_length=150)
    is_deleted = models.BooleanField(
        "Удален", default=False, help_text="Отметить если удален"
    )

    def save(self, *args, **kwargs):
        if self.is_delete is True and not self.title.endswith("Удален"):
            self.title = f"{self.title} - Удален"
        elif self.is_delete is False:
            self.title = self.title.replace("- Удален", "")
        super(GeneralHierarchy, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True
