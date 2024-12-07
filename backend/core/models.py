from django.db import models
from djangoql.admin import DjangoQLSearchMixin


class MyDjangoQLSearchMixin(DjangoQLSearchMixin):
    djangoql_completion_enabled_by_default = False
