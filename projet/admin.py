from django.contrib import admin
from .models import Utilisateur, Polygone, Projet, Noeud

# Register your models here.

class UtilisateurAdmin(admin.ModelAdmin):
	list_display=['id', 'nom', 'prenom', 'pseudo', 'mot_de_passe', 'adresse', 'telephone', 'email']
	search_fields=list_display
admin.site.register(Utilisateur, UtilisateurAdmin)

class PolygoneAdmin(admin.ModelAdmin):
	list_display=['id', 'polygone']
	search_fields=list_display
admin.site.register(Polygone, PolygoneAdmin)

class ProjetAdmin(admin.ModelAdmin):
	list_display=['id', 'nom', 'date', 'utilisateur', 'type']
	search_fields=['id', 'nom', 'date', 'type']
admin.site.register(Projet, ProjetAdmin)

class NoeudAdmin(admin.ModelAdmin):
	list_display=['identifiant_arduino', 'projet', 'altitude', 'position', 'temperature', 'radiation', 'humidite_sol']
	search_fields=['identifiant_arduino', 'altitude', 'position', 'temperature', 'radiation', 'humidite_sol']
admin.site.register(Noeud, NoeudAdmin)




