from django import forms

from crm.models import Group


class BookingGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = "__all__"
        widgets = {
            'date_checkin': forms.DateInput(attrs={'type': 'date'}),
            'date_checkout': forms.DateInput(attrs={'type': 'date'}),
        }
