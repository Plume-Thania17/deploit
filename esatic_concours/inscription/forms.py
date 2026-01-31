from django import forms
from .models import Inscription

class InscriptionForm(forms.ModelForm):
    class Meta:
        model = Inscription
        fields = [
            'nom', 'prenom', 'niveauEtude', 'email', 'etablissementOrigine',
            'concoursSouhaiter', 'extraitNaissance', 'certificatNationalite',
            'lettreMotivation', 'diplome', 'photo'
        ]
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez votre nom',
                'required': True
            }),
            'prenom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez votre prénom',
                'required': True
            }),
            'niveauEtude': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Baccalauréat série C',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'exemple@email.com',
                'required': True
            }),
            'etablissementOrigine': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de votre établissement',
                'required': True
            }),
            'concoursSouhaiter': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'extraitNaissance': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf',
                'required': True
            }),
            'certificatNationalite': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf',
                'required': True
            }),
            'lettreMotivation': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf',
                'required': True
            }),
            'diplome': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf',
                'required': True
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'required': True
            }),
        }
        labels = {
            'nom': 'Nom',
            'prenom': 'Prénom',
            'niveauEtude': 'Niveau d\'études',
            'email': 'Adresse email',
            'etablissementOrigine': 'Établissement d\'origine',
            'concoursSouhaiter': 'Concours souhaité',
            'extraitNaissance': 'Extrait de naissance',
            'certificatNationalite': 'Certificat de nationalité',
            'lettreMotivation': 'Lettre de motivation',
            'diplome': 'Diplôme',
            'photo': 'Photo d\'identité'
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Inscription.objects.filter(email=email).exists():
            raise forms.ValidationError("Cette adresse email est déjà utilisée.")
        return email

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            if photo.size > 2 * 1024 * 1024:  # 2MB
                raise forms.ValidationError("La taille de la photo ne doit pas dépasser 2 MB.")
        return photo

    def clean(self):
        cleaned_data = super().clean()
        # Add any cross-field validation here if needed
        return cleaned_data