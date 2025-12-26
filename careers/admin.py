from django.contrib import admin
from .models import JobRole


@admin.register(JobRole)
class JobRoleAdmin(admin.ModelAdmin):
    list_display = ['title', 'employment_type', 'location', 'is_active', 'created_at']
    list_filter = ['employment_type', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('title', 'slug', 'employment_type', 'location', 'is_active')
        }),
        ('Détails du poste', {
            'fields': ('description', 'responsibilities', 'requirements', 'benefits')
        }),
    )
