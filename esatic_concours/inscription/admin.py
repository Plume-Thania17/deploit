

# Register your models here.
from django.contrib import admin
from .models import Inscription

class InscriptionAdmin(admin.ModelAdmin):
    list_display = ('numero_inscription', 'nom', 'prenom', 'email', 'concoursSouhaiter', 'date_inscription')
    search_fields = ('numero_inscription', 'nom', 'prenom', 'email')
    list_filter = ('concoursSouhaiter', 'date_inscription')
    readonly_fields = ('date_inscription', 'numero_inscription')

admin.site.register(Inscription, InscriptionAdmin)