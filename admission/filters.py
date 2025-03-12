import django_filters
from .models import Student, Program  # Import models

class StudentFilter(django_filters.FilterSet):
    program = django_filters.ModelChoiceFilter(
        queryset=Program.objects.all(),  # Fetch all departments
        field_name='program',
        to_field_name='id',
        label="Program"
    )

    year_of_admission = django_filters.NumberFilter(
        field_name='year_of_admission',
        label="Year of Admission"
    )

    stud_adm_no = django_filters.ChoiceFilter(
        field_name='stud_adm_no',  # Corrected field name
        choices=lambda: Student.objects.values_list('stud_adm_no', 'stud_adm_no').distinct(),
        label="Admission No"
    )

    tc_status = django_filters.BooleanFilter(
        field_name='tc_no',
        lookup_expr='isnull',
        exclude=True,
        label="Exclude TC"
    )

    class Meta:
        model = Student
        fields = ['program', 'year_of_admission', 'stud_adm_no', 'tc_status']
