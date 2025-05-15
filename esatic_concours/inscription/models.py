from django.db import models

# Create your models here.
class Inscription(models.Model):
    CHOICES_TYPE = [
        ('licence_twin', ' TWIN'),
        ('licence_srit', 'SRIT'),
        ('master_informatique', 'MASTER INFORMATIQUE')
    ]
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    niveauEtude = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    etablissementOrigine = models.CharField(max_length=200)
    concoursSouhaiter = models.CharField(max_length=150, choices=CHOICES_TYPE)

    extraitNaissance = models.FileField(upload_to='documents/extrait/')
    certificatNationalite = models.FileField(upload_to='documents/certificat/')
    lettreMotivation = models.FileField(upload_to='documents/lettre/')
    diplome = models.FileField(upload_to='documents/diplome/')
    photo = models.ImageField(upload_to='documents/photo')

    date_inscription = models.DateTimeField(auto_now_add=True)
    numero_inscription = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
     if not self.numero_inscription:
        super().save(*args, **kwargs)  # Sauvegarde d'abord pour obtenir un ID
        self.numero_inscription = f"ESATIC-{self.concoursSouhaiter}-{self.id}"
        super().save(*args, **kwargs)  # Sauvegarde à nouveau avec le numéro
     else:
        super().save(*args, **kwargs)

    def __str__(self):
        return self.numero_inscription