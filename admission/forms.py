from django import forms
from .models import Department,Program,Student,TransferCertificate, Caste, Religion, Quota,ProgramLevel,Scholarship, StudentScholarship,Category,User,CourseCertificate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
import re

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['dept_name']
        widgets = {
            'dept_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter department name'}),
        }
class ProgramForm(forms.ModelForm):
    class Meta:
        model =Program
        fields = '__all__'
        program_level= forms.ModelChoiceField(queryset=ProgramLevel.objects.all(), required=False)
        department= forms.ModelChoiceField(queryset=Department.objects.all(), required=False)
        widgets = {
            'program_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter program name'}),

        }

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'  # Includes all fields from the model
        exclude = ['user']
        stud_reg_no = forms.CharField(required=False)  # ✅ Optional
        stud_adm_no = forms.CharField(required=False)  # ✅ Optional
        stud_roll_no = forms.CharField(required=False)  # ✅ 
        
        caste = forms.ModelChoiceField(queryset=Caste.objects.all(), required=False)
        religion = forms.ModelChoiceField(queryset=Religion.objects.all(), required=False)
        quota = forms.ModelChoiceField(queryset=Quota.objects.all(), required=False)
        category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select Category", required=True)
        normalized_mark = forms.FloatField(widget=forms.NumberInput(attrs={'step': '0.01'})) 
        photo = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'date_of_joining': forms.DateInput(attrs={'type': 'date'}),
            'egrantz': forms.CheckboxInput(),
            'status': forms.CheckboxInput(),
            
        }

    def clean_aadhaar(self):
        aadhaar = self.cleaned_data.get("aadhaar")
        
        # Format validation
        if len(aadhaar) != 12 or not aadhaar.isdigit():
            raise forms.ValidationError("Aadhaar number must be exactly 12 digits.")
        
        # Uniqueness check (excluding current record on edit)
        if Student.objects.filter(aadhaar=aadhaar).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Student with this Aadhaar number already exists.")
        
        return aadhaar

    def clean_pincode(self):
        pincode = self.cleaned_data.get("pincode")
        if len(pincode) != 6 or not pincode.isdigit():
            raise forms.ValidationError("Pincode must be 6 digits.")
        return pincode
    def clean_email(self):
        email = self.cleaned_data.get("email")
        
        # Email format check
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise forms.ValidationError("Enter a valid email address.")
        
        # Uniqueness check (exclude current record on edit)
        if Student.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Student with this Email ID already exists.")
        
        return email

    
    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if len(phone) != 10 or not phone.isdigit():
            raise forms.ValidationError("Phone number must be exactly 10 digits.")
        return phone
    def clean_parent_phone(self):
        parent_mob = self.cleaned_data.get("phone")
        if len(parent_mob) != 10 or not parent_mob.isdigit():
            raise forms.ValidationError("Phone number must be exactly 10 digits.")
        return parent_mob
from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['student', 'document_name', 'document_file']




from django import forms
from .models import TransferCertificate
from django import forms
from .models import TransferCertificate,Reason
from django.utils.timezone import now

from django import forms
from django.utils.timezone import now
from .models import TransferCertificate, Reason

class TransferCertificateForm(forms.ModelForm):
    stud_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))  
    stud_adm_no = forms.CharField(required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))  
    date_of_leaving = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    month_year = forms.CharField(
    required=True,
    widget=forms.DateInput(attrs={'type': 'month'}),
    label="Month and Year"
)


    date_of_application = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),  # Enables date picker
        initial=now().date(),
        required=False
    )

    scholarship = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    reason = forms.ModelChoiceField(
        queryset=Reason.objects.all(),
        empty_label="--Select a Reason--",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    general_conduct = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = TransferCertificate
        fields = '__all__'

        widgets = {
            'stud_name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'dob': forms.TextInput(attrs={'readonly': 'readonly'}),
            'stud_adm_no': forms.TextInput(attrs={'readonly': 'readonly'}),
            'date_of_admission': forms.TextInput(attrs={'readonly': 'readonly'}),
            'mode_of_study': forms.TextInput(attrs={'readonly': 'readonly', 'value': 'Regular'}),
            'date_of_application': forms.DateInput(attrs={'type': 'date'}),
            'date_of_leaving': forms.DateInput(attrs={'type': 'date'}),
            'month_year': forms.DateInput(attrs={'type': 'month'}),  # already handled above
            'dues_cleared': forms.Select(choices=[("Yes", "Yes"), ("No", "No")]),
            'date_of_issuing_tc': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super(TransferCertificateForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['dob'].widget.attrs.update({
                'readonly': 'readonly', 'value': self.instance.dob.strftime('%d-%m-%Y')
            })
            self.fields['date_of_admission'].widget.attrs.update({
                'readonly': 'readonly', 'value': self.instance.date_of_admission.strftime('%d-%m-%Y')
            })
            self.fields['date_of_application'].widget.attrs.update({
                'readonly': 'readonly', 'value': self.instance.date_of_application.strftime('%d-%m-%Y')
            })
            self.fields['mode_of_study'].widget.attrs.update({
                'readonly': 'readonly', 'value': 'Regular'
            })
            self.fields['date_of_issuing_tc'].initial = now().strftime("%d-%m-%Y")
            self.fields['date_of_issuing_tc'].widget.attrs['readonly'] = True

    def clean_reason(self):
        reason = self.cleaned_data.get("reason")
        if reason is None:
            raise forms.ValidationError("Please select a valid reason for TC.")
        return reason



class ScholarshipForm(forms.ModelForm):
    class Meta:
        model = Scholarship
        fields = ['name', 'scholarship_type']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Scholarship Name',
            }),
            'scholarship_type': forms.Select(attrs={
                'class': 'form-control',
            }),
        }

class StudentScholarshipForm(forms.ModelForm):
    class Meta:
        model = StudentScholarship
        fields = ['student', 'scholarship', 'amount']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'scholarship': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Amount'}),
        }

class CourseCertificateForm(forms.ModelForm):
    stud_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))  
    stud_adm_no = forms.CharField(required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))  
    programme = forms.CharField(
    label="Program",
    required=False,
    widget=forms.TextInput(attrs={
        'class': 'form-control',
        'readonly': 'readonly',
        'style': 'font-weight: bold; color: black;'
    })
)

    class Meta:
        model = CourseCertificate
        exclude = ['admission_no', 'program', 'student']

        widgets = {
            'stud_name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'stud_adm_no': forms.TextInput(attrs={'readonly': 'readonly'}),
            'programme':forms.TextInput(attrs={'readonly': 'readonly'}),
            'dob':forms.TextInput(attrs={'readonly': 'readonly'}),
            'date_of_issue': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super(CourseCertificateForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
           
            self.fields['date_of_issue'].initial = now().strftime("%d-%m-%Y")
            self.fields['date_of_issue'].widget.attrs['readonly'] = True

    


