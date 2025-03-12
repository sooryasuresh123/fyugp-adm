from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Department,Program,Student,TransferCertificate,Scholarship,StudentScholarship,Teacher
from .forms import DepartmentForm,ProgramForm,StudentForm, TransferCertificateForm,ScholarshipForm,StudentScholarshipForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout

def student_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'registration/login.html')

'''def student_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            return render(request, 'registration/login.html', {'error': 'Email and password are required'})

        try:
            user = User.objects.get(email=email)  # Get user by email
            print(f"Found user: {user}")  # Debugging

            # Authenticate using email as username and Aadhaar as password
            user = authenticate(username=user.username, password=password)
            
            if user:
                try:
                    student = Student.objects.get(user=user)  # Ensure user is a student
                    login(request, user)
                    print("Login successful")  # Debugging
                    return redirect('student_dashboard')  # Redirect to student dashboard
                except Student.DoesNotExist:
                    print("Not a student account")  # Debugging
                    return render(request, 'error.html', {'message': 'Unauthorized access.'})
            else:
                print("Invalid credentials")  # Debugging
                return render(request, 'registration/login.html', {'error': 'Invalid credentials'})

        except User.DoesNotExist:
            print("Email not found")  # Debugging
            return render(request, 'registration/login.html', {'error': 'Email not found'})

    return render(request, 'registration/login.html')'''
@login_required
def student_dashboard(request):
    try:
        student = Student.objects.get(user=request.user)  # Ensure user is a student
        return render(request, 'student_dashboard.html', {'student': student})
    except Student.DoesNotExist:
        return render(request, 'error.html', {'message': 'Unauthorized access.'})


@login_required
def office_admin_dashboard(request):
    """Dashboard view for office admins (Teachers)."""
    if request.user.is_superuser:
        return redirect('principal_dashboard')  # Redirect to principal if a superuser

    try:
        office_admin =  request.user  # Assuming Teacher is for office admins
        return render(request, 'dashboard_office_admin.html', {'office_admin': office_admin})
    except User.DoesNotExist:
        return render(request, 'error.html', {'message': 'Unauthorized access.'})

@login_required
def principal_dashboard(request):
    """Dashboard view for the principal."""
    if request.user.is_superuser:
        return render(request, 'dashboard_principal.html')
    else:
        return render(request, 'error.html', {'message': 'Unauthorized access.'})
    

'''
def index(request):
    """Redirect users to their respective dashboards after login."""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('principal_dashboard')
        else:
            try:
                if Student.objects.filter(user=request.user).exists():
                    return redirect('student_dashboard')
                elif Teacher.objects.filter(user=request.user).exists():  # Office Admin Check
                    return redirect('office_admin_dashboard')
                else:
                    return render(request, 'error.html', {'message': 'Unauthorized access.'})
            except:
                return render(request, 'error.html', {'message': 'Unauthorized access.'})
    else:
        return redirect('login')
'''

def index(request):
    """Redirect users to their respective dashboards after login based on group membership."""
    if request.user.is_authenticated:
        # Get the user's group
        user_groups = request.user.groups.all()

        if user_groups.exists():
            # Check if the user is in a specific group and redirect accordingly
            if request.user.groups.filter(name='admin').exists():
                return redirect('principal_dashboard')
            elif request.user.groups.filter(name='office').exists():
                return redirect('office_admin_dashboard')
            elif request.user.groups.filter(name='principal').exists():
                return redirect('principal_dashboard')
            else:
                # If user is in an unknown group
                return render(request, 'error.html', {'message': 'Unauthorized access. No valid group found.'})
        else:
            # User is not part of any group
            return render(request, 'error.html', {'message': 'Unauthorized access. User not in any group.'})
    else:
        # If the user is not authenticated, redirect to login
        return redirect('login')

def manage_department(request):
    departments = Department.objects.all()
    return render(request, 'manage_department.html', {'departments': departments})

def add_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_department')
    else:
        form = DepartmentForm()
    return render(request, 'add_department.html', {'form': form})

def edit_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('manage_department')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'edit_department.html', {'form': form})

def delete_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.delete()
        return redirect('manage_department')
    return render(request, 'delete_department.html', {'department': department})


def manage_program(request):
   programs = Program.objects.all()
   return render(request, 'manage_program.html', {'programs': programs})

def add_program(request):
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_program')
    else:
        form = ProgramForm()
    return render(request, 'add_program.html', {'form': form})

def edit_program(request, pk):
    program = get_object_or_404(Program, id=pk)
    if request.method == 'POST':
        form = ProgramForm(request.POST, instance=program)
        if form.is_valid():
            form.save()
            return redirect('manage_program')
    else:
        form =ProgramForm(instance=program)
    return render(request, 'edit_program.html', {'form': form,'program': program})

def delete_program(request, pk):
   program = get_object_or_404(Program,id=pk)
   if request.method == 'POST':
        program.delete()
        return redirect('manage_program')
   return render(request, 'delete_program.html', {'program': program})

def manage_student(request):
    students = Student.objects.all()
    return render(request, 'manage_student.html', {'students': students})
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("manage_student") 
        else:
               print(form.errors) # Change this to your student listing page
    else:
        form = StudentForm()

    return render(request, "add_student.html", {"form": form})
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect("manage_student")  # Redirect to student list
    else:
        form = StudentForm(instance=student)

    return render(request, "edit_student.html", {"form": form})

def delete_student(request, pk):
   student = get_object_or_404(Student, pk=pk)
   if request.method == 'POST':
        student.delete()
        return redirect('manage_student')
   return render(request, 'delete_student.html', {'student': student})


def transfer_certificate_list(request):
    tc_list = TransferCertificate.objects.all()
    return render(request, 'transfer_certificate_list.html', {'tc_list': tc_list})

def add_transfer_certificate(request):
    if request.method == 'POST':
        form = TransferCertificateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transfer_certificate_list')
    else:
        form = TransferCertificateForm()
    return render(request, 'add_transfer_certificate.html', {'form': form})
def edit_transfer_certificate(request, tc_id):
    tc = get_object_or_404(TransferCertificate, id=tc_id)
    
    if request.method == 'POST':
        form = TransferCertificateForm(request.POST, instance=tc)
        if form.is_valid():
            form.save()
            messages.success(request, "Transfer Certificate updated successfully!")
            return redirect('transfer_certificate_list')  # Redirect to TC list page
    else:
        form = TransferCertificateForm(instance=tc)

    return render(request, 'edit_transfer_certificate.html', {'form': form, 'tc': tc})
def delete_transfer_certificate(request, tc_id):
    tc = get_object_or_404(TransferCertificate, id=tc_id)
    
    if request.method == 'POST':
        tc.delete()
        messages.success(request, "Transfer Certificate deleted successfully!")
        return redirect('transfer_certificate_list')  # Redirect to TC list page
    
    return render(request, 'confirm_delete.html', {'tc': tc})



def manage_scholarships(request):
    scholarships = Scholarship.objects.all()
    return render(request, 'manage_scholarships.html')
def scholarship_details(request):
    scholarships = Scholarship.objects.all()
    return render(request, 'scholarship_details.html', {'scholarships': scholarships})

# Add Scholarship
def add_scholarship(request):
    if request.method == 'POST':
        form = ScholarshipForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('scholarship_details')
    else:
        form = ScholarshipForm()
    return render(request, 'add_scholarship.html', {'form': form})
def edit_scholarship(request, scholarship_id):
    scholarship = get_object_or_404(Scholarship, id=scholarship_id)
    if request.method == 'POST':
        form = ScholarshipForm(request.POST, instance=scholarship)
        if form.is_valid():
            form.save()
            return redirect('scholarship_details')
    else:
        form = ScholarshipForm(instance=scholarship)
    return render(request, 'edit_scholarship.html', {'form': form})

def delete_scholarship(request, scholarship_id):
    scholarship = get_object_or_404(Scholarship, id=scholarship_id)
    scholarship.delete()
    return redirect('scholarship_details')

def student_scholarships(request):
    student_scholarships = StudentScholarship.objects.all()
    return render(request, 'student_scholarships.html', {'student_scholarships': student_scholarships})

# Add Student Scholarship
def add_student_scholarship(request):
    if request.method == 'POST':
        form = StudentScholarshipForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_scholarships')
    else:
        form = StudentScholarshipForm()
    return render(request, 'add_student_scholarship.html', {'form': form})
def edit_student_scholarship(request, student_scholarship_id):
    student_scholarship = get_object_or_404(StudentScholarship, id=student_scholarship_id)
    if request.method == 'POST':
        form = StudentScholarshipForm(request.POST, instance=student_scholarship)
        if form.is_valid():
            form.save()
            return redirect('student_scholarships')
    else:
        form = StudentScholarshipForm(instance=student_scholarship)
    return render(request, 'edit_student_scholarship.html', {'form': form})

def delete_student_scholarship(request, student_scholarship_id):
    student_scholarship = get_object_or_404(StudentScholarship, id=student_scholarship_id)
    student_scholarship.delete()
    return redirect('student_scholarships')

def user_logout(request):
    logout(request)
    return redirect('login')


# def manage_qualified_marks(request):
#     qualified_marks = QualifiedMark.objects.select_related('stud','board').all()
#     return render(request, 'manage_qualified_marks.html', {'qualified_marks': qualified_marks})

# def add_qualified_mark(request):
#     if request.method == 'POST':
#         form = QualifiedMarkForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('manage_qualified_marks')
#     else:
#         form = QualifiedMarkForm()
#     return render(request, 'add_qualified_mark.html', {'form': form})

# def edit_qualified_mark(request, stud_id):
#     qualified_mark = get_object_or_404(QualifiedMark, stud_id=stud_id)
#     if request.method == 'POST':
#         form = QualifiedMarkForm(request.POST, instance=qualified_mark)
#         if form.is_valid():
#             form.save()
#             return redirect('manage_qualified_marks')
#     else:
#         form = QualifiedMarkForm(instance=qualified_mark)
#     return render(request, 'edit_qualified_mark.html', {'form': form})

# def delete_qualified_mark(request, stud_id):
#     qualified_mark = get_object_or_404(QualifiedMark, stud_id=stud_id)
    
#     if request.method == 'POST':
#         qualified_mark.delete()
#         return redirect('manage_qualified_marks')

#     return render(request, 'delete_qualified_mark.html', {'qualified_mark': qualified_mark})

# def custom_login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
        
#         if user is not None:
#             login(request, user)
#             if user.is_superuser:
                
#                 return redirect('index')  # Redirect to home page or dashboard
#         else:
#             messages.error(request, "Invalid credentials")
    
#     return render(request, 'login.html')


# def manage_users(request):
#     users = User.objects.all()
#     return render(request, 'manage_users.html', {'users': users})

# def add_user(request):
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('manage_users')
#     else:
#         form = UserForm()
#     return render(request, 'add_user.html', {'form': form})

# def edit_user(request, user_id):
#     user = get_object_or_404(User, pk=user_id)
#     if request.method == 'POST':
#         form = UserForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             return redirect('manage_users')
#     else:
#         form = UserForm(instance=user)
#     return render(request, 'edit_user.html', {'form': form})

# def delete_user(request, user_id):
#     user = get_object_or_404(User, pk=user_id)
#     if request.method == 'POST':
#         user.delete()
#         return redirect('manage_users')
#     return render(request, 'delete_user.html', {'user': user})

# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required

# @login_required
# def dashboard(request):
#     user = request.user
    
#     if user.is_student():
#         return render(request, 'dashboard.html')
    
#     elif user.is_office_admin():
#         return render(request, 'dashboard.html')
    
#     elif user.is_principal():
#         return render(request, 'dashboard.html')
    
#     else:
#         return redirect('login')  # Redirect to login if no role found
from django.shortcuts import render, get_object_or_404, redirect
from .models import Document
from .forms import DocumentForm

# List all documents
def manage_documents(request):
    documents = Document.objects.all()
    return render(request, 'manage_documents.html', {'documents': documents})

# Upload a new document
def upload_document(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_documents')  # Redirect to document list after saving
    else:
        form = DocumentForm()
    return render(request, 'document_form.html', {'form': form})

# Edit an existing document
def edit_document(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect('manage_documents')
    else:
        form = DocumentForm(instance=document)
    return render(request, 'document_form.html', {'form': form})

# Delete a document
def delete_document(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == "POST":
        document.delete()
        return redirect('manage_documents')
    return render(request, 'document_confirm_delete.html', {'document': document})
from django.shortcuts import render
from django_filters.views import FilterView
from .models import Student
from .filters import StudentFilter

from django.shortcuts import render
from .models import Student, Program

def student_list(request):
    students = Student.objects.all()  

    # Fetch available programs
    programs = Program.objects.all()  
    # Fetch distinct admission numbers
    admission_numbers = Student.objects.values_list('stud_adm_no', flat=True).distinct()
    
    # Apply filters
    program_id = request.GET.get('program')
    stud_adm_no = request.GET.get('stud_adm_no')
    year_of_admission = request.GET.get('year_of_admission')
    tc_status = request.GET.get('tc_status')  # TC Status filter

    if program_id:
        students = students.filter(program_id=program_id)
    if stud_adm_no:
        students = students.filter(stud_adm_no=stud_adm_no)
    if year_of_admission:
        students = students.filter(year_of_admission=year_of_admission)
    
    # Filter based on TC Status
    if tc_status == "exclude":
        students = students.filter(status=True)  # Exclude students with status=True
    elif tc_status == "include":
        students = students.filter(status=False)  # Include only students with status=False

    return render(request, 'student_list.html', {
        'students': students,
        'programs': programs,
        'admission_numbers': admission_numbers,
    })


def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'student_details.html', {'student': student})