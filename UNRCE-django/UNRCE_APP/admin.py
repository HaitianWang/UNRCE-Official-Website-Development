from django.contrib import admin

from .models import Image
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Project

class CustomUserAdmin(UserAdmin):
    # Define which fields are displayed on the admin page
    list_display = ('email', 'is_active', 'date_joined')
    search_fields = ('email',)
    ordering = ('email',)

    # Define fieldsets for add and change pages in admin
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    # For the add page
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )

# class ProjectAdmin(admin.ModelAdmin):
#     list_display = ("title")
#     search_fields = ("title")

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Image)
admin.site.register(Project)