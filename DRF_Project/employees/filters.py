import django_filters 
from .models import Employee

#CREAING CUSTOM FILTER LIKE  THE SERIALIZERS OR DJANGO FORMS.

class EmpployeeFilter(django_filters.FilterSet):                    #FilterSet have all the functionalities of handling filters.
    designation =  django_filters.CharFilter(field_name='designation', lookup_expr='icontains')     #icontains return result even though there is only one word matches

    class Meta:
        model = Employee
        fields = ['designation']