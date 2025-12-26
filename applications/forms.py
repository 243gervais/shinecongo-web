from django import forms
from django.core.exceptions import ValidationError
from .models import JobApplication


class JobApplicationForm(forms.ModelForm):
    """Formulaire de candidature avec validation"""
    
    class Meta:
        model = JobApplication
        fields = [
            'full_name', 'email', 'phone', 'city', 
            'position_applied', 'years_experience', 
            'availability_date', 'message', 'cv_file'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent',
                'placeholder': 'Votre nom complet'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent',
                'placeholder': 'votre.email@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent',
                'placeholder': '+243 XXX XXX XXX'
            }),
            'city': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent',
                'placeholder': 'Kinshasa'
            }),
            'position_applied': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent',
                'placeholder': 'Ex: Laveur de voitures'
            }),
            'years_experience': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent',
                'min': '0',
                'placeholder': '0'
            }),
            'availability_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent',
                'type': 'date'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent',
                'rows': '5',
                'placeholder': 'Parlez-nous de vous et pourquoi vous souhaitez rejoindre Shine Congo...'
            }),
            'cv_file': forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent',
                'accept': '.pdf,.doc,.docx'
            }),
        }
    
    def clean_cv_file(self):
        cv_file = self.cleaned_data.get('cv_file')
        if cv_file:
            # Vérifier la taille (5MB max)
            if cv_file.size > 5 * 1024 * 1024:
                raise ValidationError('La taille du fichier ne doit pas dépasser 5MB.')
            
            # Vérifier l'extension
            allowed_extensions = ['pdf', 'doc', 'docx']
            ext = cv_file.name.split('.')[-1].lower()
            if ext not in allowed_extensions:
                raise ValidationError(f'Format de fichier non accepté. Utilisez: {", ".join(allowed_extensions)}')
        
        return cv_file
