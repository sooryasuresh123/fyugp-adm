from django.contrib import admin
from .models import Department,Program,Student,Category,Caste, Religion, Quota,Scholarship,Reason, TransferCertificate,ProgramLevel,Role,ScholarshipType,Board,Pathway,DocType,Teacher,CourseCertificate

# Register your models here.
admin.site.register(Department)
admin.site.register(Program)
admin.site.register(Student)
admin.site.register(Category)
admin.site.register(Caste)
admin.site.register(Religion)
admin.site.register(Quota)
admin.site.register(Reason)
admin.site.register(TransferCertificate)
admin.site.register(ProgramLevel)
admin.site.register(Role) 
admin.site.register(Scholarship)
admin.site.register(ScholarshipType)
admin.site.register(Board)
admin.site.register(DocType)
admin.site.register(Teacher)
admin.site.register(Pathway)
admin.site.register(CourseCertificate)

# from django.contrib.auth.admin import UserAdmin
# from .models import CustomUser

# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
#     list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
#     fieldsets = (
#         (None, {'fields': ('username', 'email', 'password')}),
#         ('Permissions', {'fields': ('role', 'is_staff', 'is_active', 'groups', 'user_permissions')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'email', 'role', 'password1', 'password2', 'is_staff', 'is_active')}
#         ),
#     )
#     search_fields = ('username', 'email')
#     ordering = ('username',)

# admin.site.register(CustomUser, CustomUserAdmin)



