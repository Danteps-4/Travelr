from django import forms
from .models import Visit

class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ["date_from", "date_until"]

        widgets = {
            'date_from':forms.TextInput(attrs={'type':'date'}),
            'date_until':forms.TextInput(attrs={'type':'date'}),
        }
    
    def save(self, commit, request, country):
        visit = super().save(commit=False)
        visit.profile = request.user.profile
        visit.country = country["name"]["common"]
        if commit:
            visit.save()
        return visit

