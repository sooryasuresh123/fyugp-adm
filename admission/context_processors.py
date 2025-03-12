# from django.contrib.auth.models import Group

# def is_student(request):
#     """Check if the current user belongs to the 'HoD' group."""
#     return {'is_student': request.user.groups.filter(name='Student').exists()}
# def is_princi(request):
#     """Check if the current user belongs to the 'HoD' group."""
#     return {'is_princi': request.user.groups.filter(name='Principal').exists()}
# def is_office(request):
#     """Check if the current user belongs to the 'HoD' group."""
#     return {'is_office': request.user.groups.filter(name='Office Admin').exists()}