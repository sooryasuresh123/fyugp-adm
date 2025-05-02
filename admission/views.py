from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Department,Program,Student,TransferCertificate,Scholarship,StudentScholarship
from .forms import DepartmentForm,ProgramForm,StudentForm, TransferCertificateForm,ScholarshipForm,StudentScholarshipForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages



def student_login(request):
    if request.user.is_authenticated:
        return redirect('index')  # Already logged in

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'registration/login.html')

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
        return redirect('principal_dashboard')

    # Check if user belongs to 'office' group
    is_office = request.user.groups.filter(name='office').exists()
    is_hod = request.user.groups.filter(name='hod').exists()

    if not is_office:
        return render(request, 'error.html', {'message': 'Unauthorized access.'})

    return render(request, 'dashboard_office_admin.html', {
        'is_office': is_office,
        'is_hod': is_hod,
        'office_admin': request.user,
    })


from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def principal_dashboard(request):
    """Dashboard view for the principal."""
    is_superuser = request.user.is_superuser
    is_office = request.user.groups.filter(name='office').exists()
    is_hod = request.user.groups.filter(name='HOD').exists()

    if is_superuser:
        return render(request, 'dashboard_principal.html', {
            'is_superuser': is_superuser,
            'is_office': is_office,
            'is_hod': is_hod,
        })
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

@login_required
def hod_dashboard(request):
    is_hod = request.user.groups.filter(name='hod').exists()
    if not is_hod:
        return render(request, 'error.html', {'message': 'Unauthorized access.'})

    return render(request, 'dashboard_hod.html', {
        'is_hod': is_hod,
        'hod': request.user,
    })

def index(request):
    """Redirect users to their respective dashboards after login based on group membership."""
    if request.user.is_authenticated:
        user_groups = request.user.groups.all()

        if user_groups.exists():
            if request.user.groups.filter(name='admin').exists():
                return redirect('principal_dashboard')
            elif request.user.groups.filter(name='office').exists():
                return redirect('office_admin_dashboard')
            elif request.user.groups.filter(name='principal').exists():
                return redirect('principal_dashboard')
            elif request.user.groups.filter(name='hod').exists():   # ✅ NEW LINE
                return redirect('hod_dashboard')  # ✅ REDIRECT TO HOD DASHBOARD
            else:
                return render(request, 'error.html', {'message': 'Unauthorized access. No valid group found.'})
        else:
            return render(request, 'error.html', {'message': 'Unauthorized access. User not in any group.'})
    else:
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



from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from .models import TransferCertificate,Reason
from .models import Student
from .forms import TransferCertificateForm
from django.shortcuts import render, redirect
from django.contrib import messages

def manage_tc(request):
    tc_list = TransferCertificate.objects.all().order_by('-id')  # newest first
    return render(request, 'manage_tc.html', {'tc_list': tc_list})



def issue_tc(request):
    if request.method == "GET" and "adm_no" in request.GET:
        adm_no = request.GET.get("adm_no")
        return redirect("issue_tc_form", adm_no=adm_no)
    return render(request, "issue_tc.html")




def issue_tc_form(request, adm_no):
    student = get_object_or_404(Student, stud_adm_no=adm_no)

    last_tc = TransferCertificate.objects.order_by('-id').first()
    last_tc_number = int(last_tc.tc_no.split('/')[0]) + 1 if last_tc else 503
    tc_number = f"{last_tc_number}/2024-2025"

    if TransferCertificate.objects.filter(student=student).exists():
        messages.error(request, "TC has already been issued for this student.")
        return redirect('issue_tc')

    if request.method == "POST":
        print("Form submitted!")

        post_data = request.POST.copy()

        post_data['student'] = student.pk
        post_data['details_of_exam'] = "Kannur University"
        post_data['programme'] = student.program.pk if student.program else ''
        post_data['reg_no'] = student.stud_reg_no
        post_data['mode_of_study'] = "Regular"

        for date_field in ['dob', 'date_of_admission', 'date_of_leaving', 'date_of_application']:
            if post_data.get(date_field):
                try:
                    d = post_data[date_field].split('-')
                    if len(d[0]) == 2: 
                        post_data[date_field] = f"{d[2]}-{d[1]}-{d[0]}"
                except Exception as e:
                    print(f"Date conversion error: {e}")

        post_data['month_year'] = now().strftime('%m-%Y')
        
        form = TransferCertificateForm(post_data)
        if form.is_valid():
            tc = form.save(commit=False)
            tc.tc_no = tc_number
            tc.admission_no = student.stud_adm_no  

            tc.date_of_issuing_tc = now().date()
            tc.save()

            student.status = False
            student.save()

            messages.success(request, f"Transfer Certificate for {student.stud_name} has been successfully issued.")
            return redirect('manage_tc')
        else:
            print("Form Errors:", form.errors)

    else:
        
        initial_data = {
            'student': student.pk,
            'stud_name': student.stud_name,
            'dob': student.dob.strftime('%Y-%m-%d'),
            'stud_adm_no': student.stud_adm_no,
            'date_of_admission': student.date_of_joining.strftime('%Y-%m-%d'),
            'programme': student.program,
            'details_of_exam': "Kannur University",
            'mode_of_study': "Regular",
            'scholarship': student.egrantz if student.egrantz else "",
            'date_of_application': now().date(),
            'tc_no': tc_number,
            'reg_no': student.stud_reg_no,
            'date_of_leaving': now().date(),
            'month_year': now().strftime('%m-%Y'),
            'dues_cleared': "Yes",
            'date_of_issuing_tc': now().date(),
            'reason': getattr(student, 'reason', None),
        }

        form = TransferCertificateForm(initial=initial_data)

    return render(request, 'issue_tc_form.html', {'form': form, 'today': now().date()})

def print_tc(request, adm_no):
    tc = TransferCertificate.objects.get(admission_no=adm_no)
    return render(request, 'print_tc.html', {'tc': tc})


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
    adm_no = request.GET.get('adm_no', '').strip()  # Get admission number from search form
    if adm_no:
        student_scholarships = StudentScholarship.objects.filter(student__stud_adm_no__icontains=adm_no)
    else:
        student_scholarships = StudentScholarship.objects.all()

    return render(request, 'student_scholarships.html', {
        'student_scholarships': student_scholarships,
        'adm_no': adm_no  # Pass adm_no back to template to keep search value
    })

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


from django.shortcuts import render, get_object_or_404, redirect
from .models import Document
from .forms import DocumentForm

# List all documents
def manage_documents(request):
    adm_no = request.GET.get('adm_no', '').strip()
    documents = Document.objects.all()
    
    if adm_no:
        documents = documents.filter(student__stud_adm_no__icontains=adm_no)

    return render(request, 'manage_documents.html', {
        'documents': documents,
        'adm_no': adm_no
    })

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

from .models import Student,CourseCertificate
from .forms import CourseCertificateForm
from django.shortcuts import render, redirect
from django.contrib import messages

def manage_cc(request):
    cc_list = CourseCertificate.objects.all().order_by('-id')  # newest first
    return render(request, 'manage_cc.html', {'cc_list': cc_list})



def issue_cc(request):
    if request.method == "GET" and "adm_no" in request.GET:
        adm_no = request.GET.get("adm_no")
        return redirect("issue_cc_form", adm_no=adm_no)
    return render(request, "issue_cc.html")




def issue_cc_form(request, adm_no):
    student = get_object_or_404(Student, stud_adm_no=adm_no)

    if CourseCertificate.objects.filter(student=student).exists():
        messages.error(request, "CC has already been issued for this student.")
        return redirect('issue_cc')

    if request.method == "POST":
        print("Form submitted!")

        post_data = request.POST.copy()

        post_data['student'] = student.pk
    
        post_data['programme'] = student.program.pk if student.program else ''


        for date_field in [ 'dob','date_of_issue']:
            if post_data.get(date_field):
                try:
                    d = post_data[date_field].split('-')
                    if len(d[0]) == 2: 
                        post_data[date_field] = f"{d[2]}-{d[1]}-{d[0]}"
                except Exception as e:
                    print(f"Date conversion error: {e}")


        
        form = CourseCertificateForm(post_data)
        if form.is_valid():
            cc = form.save(commit=False)
            cc.admission_no = student.stud_adm_no  
            cc.dob=student.dob
            cc.date_of_issue = now().date()
            cc.student = student
            cc.program = student.program.program_name
            cc.save()

            student.status = False
            student.save()

            messages.success(request, f"Course Certificate for {student.stud_name} has been successfully issued.")
            return redirect('manage_cc')
        else:
            print("Form Errors:", form.errors)

    else:
        
        initial_data = {
            'student': student.pk,
            'stud_name': student.stud_name,
            'stud_adm_no': student.stud_adm_no,
            'dob': student.dob.strftime('%Y-%m-%d'),
            'programme': student.program.program_name,
            'date_of_issue': now().date(),
        }

        form = CourseCertificateForm(initial=initial_data)

    return render(request, 'issue_cc_form.html', {'form': form, 'today': now().date()})

def print_cc(request, adm_no):
    cc = CourseCertificate.objects.get(admission_no=adm_no)
    return render(request, 'print_cc.html', {'cc': cc})

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect

@login_required
def change_credentials(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        new_username = request.POST.get('new_username')

        password_changed = False
        username_changed = False

        # Password Change
        if new_password and confirm_password:
            if new_password == confirm_password:
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                password_changed = True
            else:
                messages.error(request, 'Passwords do not match.')

        # Username Change
        if new_username:
            if User.objects.filter(username=new_username).exclude(pk=request.user.pk).exists():
                messages.error(request, 'Username already exists. Please choose another one.')
            else:
                try:
                    request.user.username = new_username
                    request.user.save()
                    username_changed = True
                except IntegrityError:
                    messages.error(request, 'Username update failed due to database error.')

        if password_changed and username_changed:
            messages.success(request, 'Password and Username updated successfully.')
            return redirect('change_credentials_done')
        elif password_changed:
            messages.success(request, 'Password updated successfully.')
            return redirect('change_credentials_done')
        elif username_changed:
            messages.success(request, 'Username updated successfully.')
            return redirect('change_credentials_done')

    return render(request, 'change_credentials.html')
