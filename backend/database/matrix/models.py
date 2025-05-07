from database.core.models import BaseModel, CreatedAtMixin
from tortoise import fields
from tortoise.validators import MaxValueValidator
from utils.constants import NAME_FOR_TASK_MATRIX
from database.matrix.validators import ValidationCheckStatus, ValidationTemplateGrade


class Skill(BaseModel):
    area_of_application = fields.CharField(max_length=11)
    skill = fields.CharField(max_length=150)

    class Meta:
        table = "skill"


class GradeSkill(BaseModel):
    grade = fields.CharField(
        max_length=10,
        validators=[ValidationTemplateGrade()]
    )
    evaluation_number = fields.SmallIntField(
        validators=[MaxValueValidator(5)]
    )

    class Meta:
        table = "gradeskill"


class Matrix(CreatedAtMixin, BaseModel):
    name = fields.CharField(max_length=20, default=NAME_FOR_TASK_MATRIX)
    template_matrix = fields.ForeignKeyField(
        model_name="models.TemplateMatrix",
        on_delete=fields.CASCADE,
        related_name="matrix"
    )
    user = fields.ForeignKeyField(
        model_name="models.User",
        on_delete=fields.CASCADE,
        related_name="matrix"
    )
    status = fields.CharField(
        max_length=10,
        validators=[ValidationCheckStatus()]
    )
    skills = fields.ManyToManyField(
        model_name="models.Skill",
        through="matrix.GradeSkillMatrix",
        related_name="matrix"
    )
    last_update_status = fields.DatetimeField(null=True)
    completed_at = fields.DatetimeField(null=True)
    deadline = fields.DatetimeField(null=True)

    class Meta:
        table = "matrix"


class TemplateMatrix(CreatedAtMixin, BaseModel):
    name = fields.CharField(max_length=100)
    company = fields.ForeignKeyField(
        model_name="models.Company",
        on_delete=fields.SET_NULL,
        related_name="template_matrix",
        null=True
    )
    author = fields.ForeignKeyField(
        model_name="models.User",
        on_delete=fields.SET_NULL,
        related_name="template_matrix",
        null=True
    )
    skills = fields.ManyToManyField(
        model_name="models.Skill",
        related_name="template_matrix"
    )

    class Meta:
        table = "templatematrix"


class GradeSkillMatrix(BaseModel):
    matrix = fields.ForeignKeyField(
        model_name="models.Matrix",
        on_delete=fields.CASCADE,
        related_name="gradeskillmatrix"
    )
    skills = fields.ForeignKeyField(
        model_name="models.Skill",
        on_delete=fields.CASCADE,
        related_name="gradeskillmatrix"
    )
    grades = fields.ForeignKeyField(
        model_name="models.GradeSkill",
        on_delete=fields.CASCADE,
        related_name="gradeskillmatrix",
        default=1
    )

    class Meta:
        table = "gradeskillmatrix"
