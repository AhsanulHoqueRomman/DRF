from django.shortcuts import render
from django.http import JsonResponse
from students.models import Student

# Create your views here.

def studentsView(request):
    students =Student.objects.all()
    students_list = list(students.values())         #manually serializing the data by convert them into list .

    return JsonResponse(students_list, safe=False)       #We need use safe parameter in JsonResponse in order to allow any non-dict object to serialize. 