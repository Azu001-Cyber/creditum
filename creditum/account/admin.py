from django.contrib import admin
from . models import User


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone','pfp', 'gender','dob',)}),
        ('KYC Info', {'fields':('address','document_type','document_image','bvn_number','tin_number',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 
									'is_superuser', 'is_verified', 
									'groups', 'user_permissions')}),
    )
    search_fields = ('email',)
    ordering = ('email',)
admin.site.register(User, UserAdmin)