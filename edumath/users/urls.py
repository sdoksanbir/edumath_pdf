from django.contrib import admin
from django.urls import path, include
from users import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('teacher-list/', views.teacher_list, name='teacher_list'),
    path('student-list/', views.student_list, name='student_list'),
    path('manager-list/', views.manager_list, name='manager_list'),
    path("teacher/register/", views.register_teacher, name="register_teacher"),
    path("teacher/update/<int:pk>/", views.update_teacher, name="update_teacher"),
    path('teacher/delete/<int:teacher_id>/', views.delete_teacher, name='delete_teacher'),
    path('teacher/update-status/<int:teacher_id>/', views.update_teacher_status, name='update_teacher_status'),
    path("student/register/", views.register_student, name="register_student"),
    path("student/update/<int:pk>/", views.update_student, name="update_student"),
    path('student/delete/<int:student_id>/', views.delete_student, name='delete_student'),
    path('student/update-status/<int:student_id>/', views.update_student_status, name='update_student_status'),
    path("manager/register/", views.register_manager, name="register_manager"),
    path("manager/update/<int:pk>/", views.update_manager, name="update_manager"),
    path('manager/delete/<int:manager_id>/', views.delete_manager, name='delete_manager'),
    path('manager/update-status/<int:manager_id>/', views.update_manager_status, name='update_manager_status'),
    path('parameters/', views.parameters, name='parameters'),
    path('parameters/subject_save/', views.subject_save, name='subject_save'),
    path('parameters/subject_update/<int:subject_pk>', views.subject_update, name='subject_update'),
    path('parameters/subject_delete/<int:subject_pk>/', views.subject_delete, name='subject_delete'),
    path('parameters/subject_save/', views.subject_save, name='subject_save'),
    path('parameters/grade_save/', views.grade_save, name='grade_save'),
    path('parameters/grade_update/<int:grade_pk>', views.grade_update, name='grade_update'),
    path('parameters/grade_delete/<int:grade_pk>/', views.grade_delete, name='grade_delete'),
]
