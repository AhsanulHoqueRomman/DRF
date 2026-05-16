import django_filters 
from .models import Employee

#CREAING CUSTOM FILTER LIKE  THE SERIALIZERS OR DJANGO FORMS.

class EmployeeFilter(django_filters.FilterSet):                    #FilterSet have all the functionalities of handling filters.
    designation =  django_filters.CharFilter(field_name='designation', lookup_expr='icontains')     #icontains return result even though there is only one word matches
    emp_name = django_filters.CharFilter(field_name='emp_name', lookup_expr='icontains')
    # id = django_filters.RangeFilter(field_name='id')        #RangeFilter only works on only integer.emp_id is not integer.
    # id_min = django_filters.CharFilter(method='filter_by_id_range', label='From EMP ID')
    # id_max = django_filters.CharFilter(method='filter_by_id_range', label='To EMP ID')
    emp_id = django_filters.CharFilter(field_name='emp_id',lookup_expr='icontains')             #If we want to filter just one emp_id


    class Meta:
        model = Employee
        fields = ['designation', 'emp_name', 'emp_id']

    # def filter_by_id_range(self, queryset, name, value):
    #     if name == 'id_min':
    #         return queryset.filter(emp_id__gte = value)
    #     if name == 'id_max':
    #         return queryset.filter(emp_id__lte = value)
    #     return queryset