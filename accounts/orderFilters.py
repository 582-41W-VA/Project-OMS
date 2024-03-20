import django_filters
from django.db.models import Q

from .models import *

class OrderFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='custom_search', label='Search')
    sort_by_date = django_filters.OrderingFilter(
        fields=('date_created',),
        field_labels={'date_created': 'Date Created'}
    )

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['title', 'image', 'description', 'date_created']
        filter_overrides = {
            django_filters.CharFilter: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'widget': forms.TextInput(attrs={'placeholder': f.label}),
                },
            },
        }
        order_by = ['search', 'priority', 'status', 'sort_by_date'] 

    def custom_search(self, queryset, name, value):
        return queryset.filter(
            models.Q(id__icontains=value) | models.Q(title__icontains=value)
        )