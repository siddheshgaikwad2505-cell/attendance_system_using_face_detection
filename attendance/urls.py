from django.urls import path
from . import views


urlpatterns = [

    path('', views.dashboard, name='dashboard'),

    path('students/', views.view_students, name='students'),

    path('attendance/', views.view_attendance, name='attendance'),

    path('mark/', views.mark_attendance, name='mark'),

]