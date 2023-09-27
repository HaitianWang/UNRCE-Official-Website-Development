from django.contrib import admin

from .models import Image
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Project

# For downloading into a CSV
import csv
from django.http import HttpResponse


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

## New Admin class for 'Project' Model. Allows customisation of admin page
class ProjectAdmin(admin.ModelAdmin):
    # Allows the download of Project table as a CSV file
    actions = ["download_csv"]

    def download_csv(self, request, queryset):
        response = HttpResponse(content_type = "text/csv")
        response["Content-Disposition"] = 'attachment; filename="projects.csv"'

        writer = csv.writer(response)
        writer.writerow(["ID", "Title", "Description", "Creation", "Conclusion", "Audience", "Delivery Frequency",
                         "Language", "Web Link", "Policy Link", "Results", "Lessons Learned", "Key Messages",
                         "Relationship to RCE Activities", "Funding", "Approval", "Status"]) # specify the header

        for project in queryset:
            writer.writerow([project.id, project.title, project.description, project.created_at, 
                             project.concluded_on, project.audience, project.delivery_frequency,
                             project.language, project.web_link, project.policy_link, project.results,
                             project.lessons_learned, project.key_messages, project.relationship_to_rce_activities,
                             project.funding, project.approval, project.status])    # specify the values
        
        return response
    
    download_csv.short_description = "Download Selected Projects as CSV"


    # Display the attributes in the admin page
    list_display = ('title', 'description', 'created_at')         # Add more fields accordingly, for what you want to show
    search_fields = ['title', 'description', 'created_at']        # Add columns to search bar


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Image)
admin.site.register(Project, ProjectAdmin)