import django_filters
from django.db.models import Q
from django import forms
from django.contrib.auth.models import Group

from .models import *


class OrderFilter(django_filters.FilterSet):
    sort_by_date = django_filters.OrderingFilter(
        fields=("date_created",), label="Sort By"
    )

    order_assigned_to = django_filters.ModelChoiceFilter(
        queryset=User.objects.filter(groups__name="worker"),
        label="Assigned To",
        widget=forms.Select(),
    )

    class Meta:
        model = Order
        fields = "__all__"
        exclude = ["title", "image", "description", "date_created", "created_by"]
        filter_overrides = {
            django_filters.CharFilter: {
                "filter_class": django_filters.CharFilter,
                "extra": lambda f: {
                    "widget": forms.TextInput(attrs={"placeholder": f.label}),
                },
            },
        }
