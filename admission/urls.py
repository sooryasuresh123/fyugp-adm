from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView


urlpatterns = [
    path('',views.index,name='index'),
    path('student-login/',views. student_login, name='student_login'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('login/', views.student_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    # path('request-tc/', views.request_tc, name='request_tc'),
    # path('course-certificate/', views.course_certificate, name='course_certificate'),
    path('office-admin-dashboard/', views.office_admin_dashboard, name='office_admin_dashboard'),
    path('principal-dashboard/', views.principal_dashboard, name='principal_dashboard'),
    path('hod_dashboard/', views.hod_dashboard, name='hod_dashboard'),

    
    path('manage_department',views.manage_department,name='manage_department'),
    path('add_department',views.add_department,name='add_department'),
    path('edit_department/<int:pk>',views.edit_department,name='edit_department'),
    path('delete_department/<int:pk>',views.delete_department,name='delete_department'),
    
    path('manage_program', views.manage_program, name='manage_program'),
    path('add_program',views.add_program,name='add_program'),
    path('edit_program/<int:pk>',views.edit_program,name='edit_program'),
    path('delete_program/<int:pk>',views.delete_program,name='delete_program'),

    path('manage_students/', views.manage_student, name='manage_student'),  # View all students
    path('students/add/', views.add_student, name='add_student'),  # Add student
    path('students/edit/<int:student_id>/', views.edit_student, name='edit_student'),  # Edit student
    path('students/delete/<int:pk>/', views.delete_student, name='delete_student'),  # Delete student
   
    

    path('manage_scholarships/', views.manage_scholarships, name='manage_scholarships'),
    path('scholarship_details/', views.scholarship_details, name='scholarship_details'),
    path('add_scholarship/', views.add_scholarship, name='add_scholarship'),
    path('edit_scholarship/<int:scholarship_id>/', views.edit_scholarship, name='edit_scholarship'),
    path('delete_scholarship/<int:scholarship_id>/', views.delete_scholarship, name='delete_scholarship'),

    path('student_scholarships/', views.student_scholarships, name='student_scholarships'),
    path('add_student_scholarship/', views.add_student_scholarship, name='add_student_scholarship'),
    path('edit_student_scholarship/<int:student_scholarship_id>/', views.edit_student_scholarship, name='edit_student_scholarship'),
    path('delete_student_scholarship/<int:student_scholarship_id>/', views.delete_student_scholarship, name='delete_student_scholarship'),


    path('manage_documents/', views.manage_documents, name='manage_documents'),
    path('documents/upload/', views.upload_document, name='upload_document'),
    path('documents/edit/<int:pk>/', views.edit_document, name='edit_document'),
    path('documents/delete/<int:pk>/', views.delete_document, name='delete_document'),

    path('students/', views.student_list, name='student_list'),
    path('students/<int:student_id>/',views.student_detail, name='student_detail'),

    path('issue-tc/', views.issue_tc, name='issue_tc'),
    path('issue-tc/<str:adm_no>/', views.issue_tc_form, name='issue_tc_form'),
    path('print-tc/<int:adm_no>/', views.print_tc, name='print_tc'),
    path('manage-tc/', views.manage_tc, name='manage_tc'),

    path('issue-cc/', views.issue_cc, name='issue_cc'),
    path('issue-cc/<str:adm_no>/', views.issue_cc_form, name='issue_cc_form'),
    path('print-cc/<int:adm_no>/', views.print_cc, name='print_cc'),
    path('manage-cc/', views.manage_cc, name='manage_cc'),

     path('change-credentials/', views.change_credentials, name='change_credentials'),
    path('change-credentials-done/', TemplateView.as_view(template_name='change_credentials_done.html'), name='change_credentials_done'),

]





  