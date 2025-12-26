from django.contrib import admin
from django.utils.html import format_html
from .models import JobApplication


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'date_of_birth', 'physical_address', 'phone', 'city', 'cv_link', 'reviewed', 'applied_at']
    list_filter = ['reviewed', 'city', 'applied_at']
    search_fields = ['full_name', 'physical_address', 'phone', 'city']
    date_hierarchy = 'applied_at'
    readonly_fields = ['applied_at']
    
    fieldsets = (
        ('Informations du candidat', {
            'fields': ('full_name', 'date_of_birth', 'physical_address', 'phone', 'city')
        }),
        ('Détails de la candidature', {
            'fields': ('message', 'cv_file')
        }),
        ('Gestion interne', {
            'fields': ('reviewed', 'notes', 'applied_at'),
            'classes': ('collapse',)
        }),
    )
    
    def cv_link(self, obj):
        if obj.cv_file:
            return format_html('<a href="{}" target="_blank">Télécharger CV</a>', obj.cv_file.url)
        return "Aucun CV"
    cv_link.short_description = "CV"
    
    actions = ['mark_as_reviewed', 'mark_as_unreviewed']
    
    def mark_as_reviewed(self, request, queryset):
        updated = queryset.update(reviewed=True)
        self.message_user(request, f'{updated} candidature(s) marquée(s) comme examinée(s).')
    mark_as_reviewed.short_description = "Marquer comme examiné"
    
    def mark_as_unreviewed(self, request, queryset):
        updated = queryset.update(reviewed=False)
        self.message_user(request, f'{updated} candidature(s) marquée(s) comme non examinée(s).')
    mark_as_unreviewed.short_description = "Marquer comme non examiné"
