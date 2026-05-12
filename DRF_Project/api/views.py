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
@api_view(['GET','POST'])
def studentsView(request):
    if request.method == 'GET':
        #Get all the data of Student table
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer  = StudentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def studentsDetailView(request, pk):
    try:
        student = Student.objects.get(pk = pk)
    except Student.DoesNotExist:
        return Response(status= status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = StudentSerializer(student, data = request.data)
