import django_filters
from django.db.models import Q

from .models import *

class OrderFilter(django_filters.FilterSet):
    sort_by_date = django_filters.OrderingFilter(
        fields=('date_created',),
        label='Sort By'
    )


    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['title', 'image', 'description', 'date_created', 'created_by']
        filter_overrides = {
            django_filters.CharFilter: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'widget': forms.TextInput(attrs={'placeholder': f.label}),
                },
            },
        }
        

    def custom_search(self, queryset, name, value):
        return queryset.filter(
            models.Q(id__icontains=value) | models.Q(title__icontains=value)
        )