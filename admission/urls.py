from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views


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
   
    path('transfer-certificates/', views.transfer_certificate_list, name='transfer_certificate_list'),
    path('add-transfer-certificate/', views.add_transfer_certificate, name='add_transfer_certificate'),
    path('edit-transfer-certificate/<int:tc_id>/', views.edit_transfer_certificate, name='edit_transfer_certificate'),
    path('delete-transfer-certificate/<int:tc_id>/', views.delete_transfer_certificate, name='delete_transfer_certificate'),


    path('manage_scholarships/', views.manage_scholarships, name='manage_scholarships'),
    path('scholarship_details/', views.scholarship_details, name='scholarship_details'),
    path('add_scholarship/', views.add_scholarship, name='add_scholarship'),
    path('edit_scholarship/<int:scholarship_id>/', views.edit_scholarship, name='edit_scholarship'),
    path('delete_scholarship/<int:scholarship_id>/', views.delete_scholarship, name='delete_scholarship'),

    path('student_scholarships/', views.student_scholarships, name='student_scholarships'),
    path('add_student_scholarship/', views.add_student_scholarship, name='add_student_scholarship'),
    path('edit_student_scholarship/<int:student_scholarship_id>/', views.edit_student_scholarship, name='edit_student_scholarship'),
    path('delete_student_scholarship/<int:student_scholarship_id>/', views.delete_student_scholarship, name='delete_student_scholarship'),


    # path('manage_users/', views.manage_users, name='manage_users'),
    # path('add_user/', views.add_user, name='add_user'),
    # path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    # path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),


    # path('qualified_marks/',views. manage_qualified_marks, name='manage_qualified_marks'),
    # path('qualified_marks/add/',views.add_qualified_mark, name='add_qualified_mark'),
    # path('qualified_marks/edit/<int:stud_id>/',views.edit_qualified_mark, name='edit_qualified_mark'),
    # path('qualified_marks/delete/<int:stud_id>/',views.delete_qualified_mark, name='delete_qualified_mark'),
    path('manage_documents/', views.manage_documents, name='manage_documents'),
    path('documents/upload/', views.upload_document, name='upload_document'),
    path('documents/edit/<int:pk>/', views.edit_document, name='edit_document'),
    path('documents/delete/<int:pk>/', views.delete_document, name='delete_document'),

    path('students/', views.student_list, name='student_list'),
    path('students/<int:student_id>/',views.student_detail, name='student_detail'), 

]
  