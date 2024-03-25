import django_filters
from django.db.models import Q

from .models import *

class UserFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='custom_search', label='Search')

    class Meta:
        model = User
        fields = []

    def custom_search(self, queryset, name, value):
        return queryset.filter(
            Q(id__icontains=value) | 
            Q(username__icontains=value) | 
            Q(email__icontains=value)
        )