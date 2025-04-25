from django.db import models
from django.contrib.auth.models import AbstractUser, Group , Permission,User
from django.core.exceptions import ValidationError





class Department(models.Model):
    dept_name = models.CharField(max_length=100, unique=True)


    def __str__(self):
        return self.dept_name
class ProgramLevel(models.Model):
    level_name = models.CharField(max_length=100,default='UG')

    def __str__(self):
        return self.level_name

class Program(models.Model):
    program_name = models.CharField(max_length=100, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True)  # ForeignKey to Department
    program_level = models.ForeignKey(ProgramLevel, on_delete=models.SET_NULL, blank=True, null=True)  # ForeignKey to ProgramLevel

    def __str__(self):
        return self.program_name
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True,default='Null')

    def __str__(self):
        return self.name
class Caste(models.Model):
    caste_name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.caste_name


class Religion(models.Model):
    religion_name = models.CharField(max_length=50)

    def __str__(self):
        return self.religion_name


class Quota(models.Model):
    quota_name = models.CharField(max_length=50)

    def __str__(self):
        return self.quota_name
class Pathway(models.Model):
    pathway_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.pathway_name

def validate_file_size(value):
    """Validate that file size is less than 50KB (for photo only)."""
    limit = 50* 1024 * 1024  # 50KB
    if value.size > limit:
        raise ValidationError("File size should not exceed 50KB.")
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,default=None)
    
    def __str__(self):
        return self.user.username


class Board(models.Model):
    board_name = models.CharField(max_length=255, unique=True)
    max_mark = models.PositiveIntegerField()

    def __str__(self):
        return self.board_name
class Reason(models.Model):
    reason_description = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.reason_description  

# class TransferCertificate(models.Model):
#     tc_no = models.CharField(max_length=50, unique=True)
#     stud = models.ForeignKey('admission.Student', on_delete=models.CASCADE)  # Assuming 'student' is your app name
#     date_of_application = models.DateField()
#     date_of_issue = models.DateField(null=True, blank=True)
#     reason = models.ForeignKey(Reason, on_delete=models.SET_NULL, null=True)

#     def __str__(self):
#         return f"TC {self.tc_no} - {self.stud}"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,default=None)
    stud_name = models.CharField(max_length=100)
    stud_adm_no = models.CharField(max_length=20, unique=True)
    stud_reg_no = models.CharField(max_length=20, unique=True, blank=True, null=True) 
    stud_roll_no = models.CharField(max_length=20, unique=True, blank=True, null=True)
    aadhaar = models.CharField(max_length=12, unique=True)
    abc_id = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    dob = models.DateField()
    caste = models.ForeignKey(Caste, on_delete=models.SET_NULL, blank=True, null=True)  # Foreign Key to Caste
    religion = models.ForeignKey(Religion, on_delete=models.SET_NULL, blank=True, null=True)  # Foreign Key to Religion
    quota = models.ForeignKey(Quota, on_delete=models.SET_NULL, blank=True, null=True)  
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)  
    program= models.ForeignKey(Program, on_delete=models.SET_NULL, blank=True, null=True)  # Foreign Key to Quota# Foreign Key to Quota
    pathway= models.ForeignKey(Pathway, on_delete=models.SET_NULL, blank=True, null=True)  # Foreign Key to Quota# Foreign Key to Quota
    board=models.ForeignKey(Board, on_delete=models.SET_NULL, blank=True, null=True)
    normalized_mark = models.FloatField(default=0.0)
    parent_name = models.CharField(max_length=100)
    parent_mob = models.CharField(max_length=15)
    house_name = models.CharField(max_length=100)
    post = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    date_of_joining = models.DateField()
    income = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    egrantz = models.BooleanField(default=False)
    status = models.BooleanField(default=True)  # Active/Inactive
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    blood_group = models.CharField(max_length=5, choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B-'), ('O+', 'O-'), ('AB+', 'AB-')])
    language=models.CharField(max_length=10, choices=[('Malayalam', 'Malayalam'), ('Hindi', 'Hindi')] ,default='Malayalam')
    identification_mark = models.TextField(blank=True, null=True)

    year_of_admission = models.IntegerField(default=2025)

    
    from django.core.validators import FileExtensionValidator
    photo = models.ImageField(
        upload_to='student_photos/', 
        blank=True, 
        null=True, 
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )
   
    def save(self, *args, **kwargs):
        # If student does not have an associated user, create one
        if not self.user:
            if User.objects.filter(username=self.email).exists():
                raise ValidationError("User with this email already exists.")

            user = User.objects.create_user(username=self.email, email=self.email, password=self.aadhaar)
            self.user = user

            # Add user to "Student" group in Django Admin (Create group if it doesn't exist)
            # student_group, created = Group.objects.get_or_create(name='Student')
            # user.groups.add(student_group)

            user.save()

        super(Student, self).save(*args, **kwargs)
    def __str__(self):
     return f"{self.stud_name} - {self.stud_adm_no}"

from django.db import models # Importing the Student model
class DocType(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Unique document type name

    def __str__(self):
        return self.name


class Document(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # Foreign key to Student table
    document_name = models.ForeignKey(DocType, on_delete=models.CASCADE)  # Document name
    document_file = models.FileField(upload_to='documents/')  # File upload field
    
    def __str__(self):
        return f"{self.student.stud_name} - {self.document_name}"
  


class ScholarshipType(models.Model):
    type_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.type_name


class Scholarship(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Scholarship Name
    scholarship_type = models.ForeignKey(ScholarshipType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
class StudentScholarship(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.student} - {self.scholarship.name} - ₹{self.amount}"

    


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name





from django.db import models
from django.utils.timezone import now

class TransferCertificate(models.Model):
    tc_no = models.CharField(max_length=20, unique=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    dob = models.DateField()
    admission_no = models.CharField(max_length=20,null=True, blank=True)
    date_of_admission = models.DateField()  # Allowing NULL
    programme = models.CharField(max_length=255, default="Not Specified")
    # details_of_exam = models.CharField(max_length=255, default="Kannur University")  # ✅ Add this field
    details_of_exam  = models.TextField(default="Kannur University")
    scholarship = models.CharField(max_length=225, blank=True, null=True)
    reason = models.ForeignKey(Reason, on_delete=models.SET_NULL, null=True, blank=False)  # ✅ Dropdown Selection

    date_of_application = models.DateField(default=now)
    date_of_issuing_tc = models.DateField(default=now)
    
    mode_of_study = models.CharField(max_length=20, default="Regular")
    date_of_leaving = models.DateField(null=True, blank=True,default=now)
    reg_no = models.CharField(max_length=20, blank=True, null=True)
    month_year = models.CharField(max_length=7)
    dues_cleared = models.CharField(
        max_length=3,
        choices=[("Yes", "Yes"), ("No", "No")],
        default="Yes"
    )


    def save(self, *args, **kwargs):
        if not self.tc_no:
            last_tc = TransferCertificate.objects.order_by('-id').first()
            if last_tc:
                last_tc_no = int(last_tc.tc_no.split('/')[0]) + 1
            else:
                last_tc_no = 503
            self.tc_no = f"{last_tc_no}/2024-2025"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"TC {self.tc_no} - {self.student.stud_name}"
from django.db import models
from datetime import date


class CourseCertificate(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='course_certificates')
    dob = models.DateField()
    admission_no = models.CharField(max_length=50)
    program = models.CharField(max_length=100)
    date_of_issue = models.DateField()

  
    def __str__(self):
        return f"Course Certificate for {self.student.stud_name} "
