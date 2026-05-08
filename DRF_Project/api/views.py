from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def studentsView(request):
    students ={
        'id' : 1,
        'name' : 'Romman',
        'Department' : 'CSE',
        'Faculty' : 'FSIT'
    }

    return JsonResponse(students)