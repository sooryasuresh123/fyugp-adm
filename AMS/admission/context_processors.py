# student/context_processors.py (or any app of your choice)
from django.contrib.auth.models import Group

def user_groups(request):
    # Check the user's groups to determine their roles
    is_office = request.user.groups.filter(name='office').exists()
    is_hod = request.user.groups.filter(name='hod').exists()
    is_superuser = request.user.is_superuser

    return {
        'is_office': is_office,
        'is_hod': is_hod,
        'is_superuser': is_superuser
    }
