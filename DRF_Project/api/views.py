from django.shortcuts import render
from django.http import JsonResponse
from students.models import Student
from .serializers import StudentSerializer
from rest_framework.response import Response
from rest_framework import  status
from rest_framework.decorators import api_view

# Create your views here.

#Manually Serailizing object Data:

# def studentsView(request):
#     students =Student.objects.all()
#     students_list = list(students.values())         #manually serializing the data by convert them into list .

#     return JsonResponse(students_list, safe=False)       #We need use safe parameter in JsonResponse in order to allow any non-dict object to serialize. 


#Serializing Objects using django rest_framework serializers.--Industry standard.
@api_view(['GET'])
def studentsView(request):
    if request.method == 'GET':
        #Get all the data of Student table
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
