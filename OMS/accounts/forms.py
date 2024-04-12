from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django import forms
from .models import Order


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = [
            "title",
            "image",
            "description",
            "priority",
            "status",
            "order_assigned_to",
        ]


class CreateUserForm(UserCreationForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Select Role",
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "groups"]


class UpdateUserForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = User
        fields = ["groups"]
