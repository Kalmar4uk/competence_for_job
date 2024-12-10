from django import forms

from matrix.models import Competence


class CompetenceForm(forms.ModelForm):

    class Meta:
        model = Competence
        fields = "__all__"
