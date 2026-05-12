from django.urls import path
from . import views

urlpatterns = [
    path('students/', views.studentsView, name= 'studentsView'),
    path('students/<int:pk>', views.studentsDetailView),
]

