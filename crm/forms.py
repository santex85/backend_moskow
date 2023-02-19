from django import forms

from crm.models import Group, Groceries, Household


class BookingGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = "__all__"
        widgets = {
            "date_checkin": forms.DateInput(attrs={"type": "date"}),
            "date_checkout": forms.DateInput(attrs={"type": "date"}),
        }


class KitchenForm(forms.ModelForm):
    class Meta:
        model = Groceries
        fields = "__all__"


class KitchenUpdateForm(forms.ModelForm):
    class Meta:
        model = Groceries
        fields = ["how_many_unit", "price"]


class HouseholdForm(forms.ModelForm):
    class Meta:
        model = Household
        fields = "__all__"


class HouseholdUpdateForm(forms.ModelForm):
    class Meta:
        model = Groceries
        fields = ["how_many_unit", "price"]
