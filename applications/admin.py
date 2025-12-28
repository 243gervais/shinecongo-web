from django.contrib import admin
from django.utils.html import format_html
from .models import JobApplication


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'application_type', 'phone', 'city', 'how_heard_about', 'cv_link', 'reviewed', 'applied_at']
    list_filter = ['reviewed', 'application_type', 'city', 'sexe', 'how_heard_about', 'applied_at']
    search_fields = ['nom', 'post_nom', 'prenom', 'full_name', 'physical_address', 'phone', 'city', 'nationalite']
    date_hierarchy = 'applied_at'
    readonly_fields = ['applied_at']
    
    fieldsets = (
        ('Type de candidature', {
            'fields': ('application_type',)
        }),
        ('Informations personnelles', {
            'fields': ('nom', 'post_nom', 'prenom', 'full_name', 'date_of_birth', 'lieu_de_naissance', 
                      'sexe', 'nationalite', 'physical_address', 'phone', 'city')
        }),
        ('Comment avez-vous connu Shine Congo', {
            'fields': ('how_heard_about', 'how_heard_details')
        }),
        ('Études et compétences', {
            'fields': ('education', 'skills', 'languages')
        }),
        ('CV et message', {
            'fields': ('cv_file', 'message')
        }),
        ('Gestion interne', {
            'fields': ('reviewed', 'notes', 'applied_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_name(self, obj):
        if obj.nom and obj.prenom:
            return f"{obj.prenom} {obj.nom} {obj.post_nom}".strip()
        elif obj.full_name:
            return obj.full_name
        return "N/A"
    get_name.short_description = "Nom"
    
    def cv_link(self, obj):
        if obj.cv_file:
            return format_html(
                '<a href="{}" target="_blank">📎 Télécharger CV</a>', 
                obj.cv_file.url
            )
        elif obj.application_type == 'MANUAL':
            from django.urls import reverse
            cv_url = reverse('applications:view_cv_pdf', args=[obj.pk])
            return format_html(
                '<a href="{}" target="_blank" style="color: #2A9D8F; font-weight: bold;">📄 Voir CV PDF</a>',
                cv_url
            )
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
