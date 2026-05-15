from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('employees', views.Employees , basename='employee' ) #We have to declare basename only when we use viewsets.ViewSet. If we use viewsets.ModelviewSet we dont have to use basename.

urlpatterns = [
    path('students/', views.studentsView, name= 'studentsView'),
    path('students/<int:pk>', views.studentsDetailView),

    # path('employees/', views.Employees.as_view()),
    # path('employees/<int:pk>', views.EmployeeDeatil.as_view()),
    path('', include(router.urls))
]

