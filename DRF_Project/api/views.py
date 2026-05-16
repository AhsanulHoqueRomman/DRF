from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from students.models import Student
from .serializers import StudentSerializer,EmployeeSerializer
from rest_framework.response import Response
from rest_framework import  status, mixins, generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from employees.models import Employee
from django.http import Http404
from blogs.models import Blog, Comment
from blogs.serializers import BlogSerializer, CommentSerializer
from .paginations import CustomPagination
from employees.filters import EmpployeeFilter

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
        # print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','PUT','DELETE'])
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
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data ,status=status.HTTP_200_OK)
        
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#All the above views are function-based views.



#Class-based views-

'''

class Employees(APIView):
    def get(self, request):
        employee = Employee.objects.all()
        serializer = EmployeeSerializer(employee, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = EmployeeSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EmployeeDeatil(APIView):
    def get_object(self, pk):
        try:
            return Employee.objects.get(pk = pk)
        except Employee.DoesNotExist():
            raise Http404

    def get(self,request, pk):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee , data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        employee = self.get_object(pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

        
'''

#Above are the class based views and to write less code we need mixins. ListModelMixin,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin.

'''

class Employees(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get(self, request):
        return self.list(request)
    
    def post(self, request):
        return self.create(request)


class EmployeeDeatil(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)
    
    def put(self, request, pk):
        return self.update(request, pk)
    
    def delete(self, request, pk):
        return self.destroy(request, pk)

'''

#Generics give us some pre-built APIView classes and functions to do this same task with less lines of code.
'''
ListAPIView,CreateAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView individually.
ListCreateAPIView - For listing and creating objects
RetrieveUpdateAPIView - For retrieving single object and updating object using pk
RetrieveUpdateDestroyAPIView - For retrieving single object and updating object and deleting objects using pk

'''
#These generics views will automatially implement all the standard CRUD operations
'''

class Employees(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer 



class EmployeeDeatil(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer 
    lookup_field = "pk"

'''

'''
By Using Mixins and Generics we reduce the lines of codes significantly.But we still have to write 2 class to to handle the standard CRUD operations.
In Django Rest Framework We have another super powerful module named- ViewSet. It's a set of views which combines the functionalitites of
views and serializers making it even more easier to perform standard CRUD operations.
We have 2 types of implementation process of viewsets:
1.We can extend 'viewsets.ViewSet' - we will have to provide these in-built functions such as: list(),create(),retrieve(),update(),delete(). 
                                     One view class will handle all of these operations.
2.Or we can extend 'viewsets.ModelViewSet'- It just takes only queryset and serializer_class and automatically provides both 
                                            pk-based and non pk-based operations.This ViewSet work with routers.Django Rest Framework provides 
                                            us a router class that automatically determines the url pattern for us.We can not use traditional urls routes.

'''

#Process-1 : viewsets.ViewSet(So many lines of code required)

'''

class Employees(viewsets.ViewSet):
    def list(self, request):
        queryset = Employee.objects.all()
        serializer = EmployeeSerializer(queryset, many =True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = EmployeeSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(employee)
        return Response (serializer.data, status=status.HTTP_200_OK)
    

    def update(self, request, pk= None):
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(employee, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        employee = get_object_or_404(Employee, pk=pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

'''
    
#Process -2 : viewsets.ModelViewSet:

class Employees(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer   #[That's it. ModelViewSet Will automatically provide all pk and non-pk based operations.] 
    pagination_class = CustomPagination
    # filterset_fields = ['designation']      #Used when We implemented global filter.
    filterset_class = EmpployeeFilter



#Below are Blog app views :

class BlogsView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class CommentsView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer    

class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'pk'

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'pk'
