from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime
from .models import JobApplication


class JobApplicationForm(forms.ModelForm):
    """Formulaire de candidature avec validation"""
    
    # Override date_of_birth to accept text input
    date_of_birth = forms.CharField(
        label="Date de naissance",
        required=True,
        help_text="Format: JJ/MM/AAAA (ex: 15/01/1990) ou en texte (ex: 15 janvier 1990)"
    )
    
    class Meta:
        model = JobApplication
        fields = [
            'full_name', 'physical_address', 'phone', 'city', 
            'date_of_birth', 'message', 'cv_file'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent',
                'placeholder': 'Votre nom complet'
            }),
            'physical_address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent',
                'rows': '3',
                'placeholder': 'Votre adresse complète (rue, quartier, commune)'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent',
                'placeholder': '+243 XXX XXX XXX'
            }),
            'city': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent',
                'placeholder': 'Kinshasa'
            }),
            'date_of_birth': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent',
                'placeholder': 'Ex: 15/01/1990 ou 15 janvier 1990'
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
    
    def clean_date_of_birth(self):
        """Clean and parse date of birth from text input"""
        from datetime import date
        from django.utils import timezone
        
        date_value = self.cleaned_data.get('date_of_birth')
        
        # If it's already a date object, just validate it
        if isinstance(date_value, date):
            parsed_date = date_value
        else:
            # It's a string, parse it
            if not date_value:
                raise ValidationError('La date de naissance est requise.')
            
            # Convert to string if it's not already
            date_str = str(date_value).strip() if date_value else ''
            if not date_str:
                raise ValidationError('La date de naissance est requise.')
            
            # Try different date formats
            date_formats = [
                '%d/%m/%Y',      # 15/01/1990
                '%d-%m-%Y',      # 15-01-1990
                '%d %m %Y',      # 15 01 1990
                '%d/%m/%y',      # 15/01/90
                '%Y-%m-%d',      # 1990-01-15
            ]
            
            parsed_date = None
            
            for fmt in date_formats:
                try:
                    parsed_date = datetime.strptime(date_str, fmt).date()
                    break
                except ValueError:
                    continue
            
            if parsed_date is None:
                # If no format worked, try to parse common French month names
                try:
                    # Try French month names
                    months_fr = {
                        'janvier': '01', 'février': '02', 'mars': '03', 'avril': '04',
                        'mai': '05', 'juin': '06', 'juillet': '07', 'août': '08',
                        'septembre': '09', 'octobre': '10', 'novembre': '11', 'décembre': '12'
                    }
                    parts = date_str.lower().split()
                    if len(parts) >= 3:
                        day = parts[0].zfill(2)
                        month = months_fr.get(parts[1], parts[1])
                        year = parts[2]
                        if len(year) == 2:
                            year = '20' + year if int(year) < 50 else '19' + year
                        parsed_date = datetime.strptime(f'{day}/{month}/{year}', '%d/%m/%Y').date()
                except (ValueError, KeyError, IndexError, AttributeError):
                    pass
            
            if parsed_date is None:
                raise ValidationError('Format de date invalide. Utilisez: JJ/MM/AAAA (ex: 15/01/1990) ou en texte (ex: 15 janvier 1990)')
        
        # Validate reasonable date (not in future, not too old)
        today = timezone.now().date()
        if parsed_date > today:
            raise ValidationError('La date de naissance ne peut pas être dans le futur.')
        if parsed_date.year < 1900:
            raise ValidationError('Veuillez entrer une date de naissance valide.')
        
        return parsed_date
    
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
