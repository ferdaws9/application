# coding=ISO-8859-1
from projet.models import Projet as ModelProjet, Utilisateur
from datetime import date
from django import forms
import datetime

class Projet(forms.Form):
	TYPE_PROJET=(
		#("O", "Predire une surface en utilisant les fonctionnalites de openweather et les noeuds."),
		("N", "Predire une surface en utilisant les fonctionnalites de openweather et les noeuds."),
		#("P", "Superviser une plante (Presence d'un noeud au moins est obligatoire!)"),
	)
	nom=forms.CharField(label='Nom du projet', max_length=ModelProjet._meta.get_field('nom').max_length, required=False, widget=forms.TextInput(attrs={'placeholder': 'Nom'}))
	type=forms.ChoiceField(label="L'objectif de ce projet est", choices=TYPE_PROJET, widget=forms.RadioSelect(), required=False)
	

	def __init__(self, *args, **kwargs):
		self.nom=kwargs.pop('nom', None)
		self.type=kwargs.pop('type', None)
		super(Projet, self).__init__(*args, **kwargs)

	def is_valid(self):
		nom=self.data['nom']
		if not nom:
			self.add_error("nom", "Champ Nom vide!")
		type=self.data.get('type', None)
		if not type:
			self.add_error("type", "Choisir un choix!")
		return super(Projet, self).is_valid()

	def enregistrer(self, pseudo):
		nom=self.cleaned_data['nom']
		type=self.cleaned_data['type']
		projet=ModelProjet.create(nom=nom, pseudo=pseudo, type=type)
		return projet
