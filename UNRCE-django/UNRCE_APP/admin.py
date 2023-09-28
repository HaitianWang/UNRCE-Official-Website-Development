from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Project, Image, SDG

class InterestedProjectsInline(admin.TabularInline):
    model = CustomUser.interested_projects.through

class InterestedSDGsInline(admin.TabularInline):
    model = CustomUser.interested_sdgs.through
    extra = 1  # Default number of empty forms to display


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'is_active', 'date_joined', 'interested_projects_list', 'interested_sdgs_list')
    search_fields = ('email', 'interested_projects__title', 'date_joined')  

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
    # Exclude the 'interested_projects' from the main user form
    exclude = ('interested_projects', )

    filter_horizontal = ('interested_projects', 'interested_sdgs')

    # Add the new inline
    inlines = [InterestedProjectsInline, InterestedSDGsInline]
    
    # Exclude the new field from the main form
    exclude = ('interested_projects', 'interested_sdgs')

    def interested_sdgs_list(self, obj):
        return ", ".join([str(sdg) for sdg in obj.interested_sdgs.all()])
    interested_sdgs_list.short_description = 'Interested SDGs'


    def interested_projects_list(self, obj):
        return ", ".join([str(project) for project in obj.interested_projects.all()])
    interested_projects_list.short_description = 'Interested Projects'

    # Inside CustomUserAdmin class

    def get_search_results(self, request, queryset, search_term):
    # Get the filtered queryset from the original method
        qs, use_distinct = super().get_search_results(request, queryset, search_term)

        project_search = request.GET.getlist('project_search')
        sdg_search = request.GET.getlist('sdg_search')

        if project_search:
            qs = qs.filter(interested_projects__id__in=project_search)

        if sdg_search:
            qs = qs.filter(interested_sdgs__id__in=sdg_search)

        return qs, use_distinct

    def changelist_view(self, request, extra_context=None):
    # Fetch all projects and SDGs to be used in the custom search form
        extra_context = extra_context or {}
        extra_context['projects'] = Project.objects.all()
        extra_context['sdgs'] = SDG.objects.all()  # Assuming you have an SDG model
    
        return super(CustomUserAdmin, self).changelist_view(request, extra_context=extra_context)

# Specify the overridden change_list template location

    

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Image)
admin.site.register(Project)
