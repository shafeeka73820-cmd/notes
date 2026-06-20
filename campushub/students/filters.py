import django_filters
from .models import Student


class StudentFilter(django_filters.FilterSet):
    min_marks = django_filters.NumberFilter(field_name='marks', lookup_expr='gte')
    max_marks = django_filters.NumberFilter(field_name='marks', lookup_expr='lte')
    dept = django_filters.CharFilter(field_name='department__name', lookup_expr='iexact')
    search = django_filters.CharFilter(method='filter_search')

    def filter_search(self, queryset, name, value):
        from django.db.models import Q
        return queryset.filter(
            Q(name__icontains=value) | Q(email__icontains=value)
        )

    class Meta:
        model = Student
        fields = ['department', 'is_active', 'branch']
