# coding=ISO-8859-1
from projet.models import Utilisateur
from projet import mot_de_passe_hash
from django import forms

class Profile(forms.Form):
	pseudo=forms.CharField(label='Pseudo', max_length=Utilisateur._meta.get_field('pseudo').max_length, required=False, widget=forms.TextInput(attrs={'placeholder': 'Pseudo', 'disabled': 'true'}))
	email=forms.CharField(label='Email', max_length=Utilisateur._meta.get_field('email').max_length, required=False, widget=forms.TextInput(attrs={'placeholder': 'E-Mail', 'disabled': 'true'}))
	nom=forms.CharField(label='Nom', max_length=Utilisateur._meta.get_field('nom').max_length, required=False, widget=forms.TextInput(attrs={'placeholder': 'Nom'}))
	prenom=forms.CharField(label='Prenom', max_length=Utilisateur._meta.get_field('prenom').max_length, required=False, widget=forms.TextInput(attrs={'placeholder': 'Prenom'}))
	adresse=forms.CharField(label='adresse', max_length=Utilisateur._meta.get_field('adresse').max_length, required=False, widget=forms.TextInput(attrs={'id': 'searchTextField', 'placeholder': 'Saisir une adresse', 'class': 'form-control', 'autocomplete': 'on', 'runat': 'server'}))
	telephone=forms.CharField(label='Telephone', max_length=20, required=False, widget=forms.TextInput(attrs={'placeholder': 'Téléphone'}))

	def __init__(self, *args, **kwargs):
		self.nom=kwargs.pop('nom', None)
		self.prenom=kwargs.pop('prenom', None)
		self.pseudo=kwargs.pop('pseudo', None)
		self.email=kwargs.pop('email', None)
		self.telephone=kwargs.pop('telephone', None)
		self.adresse=kwargs.pop('adresse', None)
		super(Profile, self).__init__(*args, **kwargs)

	def is_valid(self):
		nom=self.data['nom']
		if not nom:
			self.add_error("nom", "Nom est vide!")
		elif any(char.isdigit() for char in nom):
			self.add_error("nom", "Nom est incorrect!")
		prenom=self.data['prenom']
		if not prenom:
			self.add_error("prenom", "Prenom est vide!")
		elif any(char.isdigit() for char in prenom):
			self.add_error("prenom", "Prenom est incorrect!")
		telephone=self.data['telephone']
		if not telephone:
			self.add_error("telephone", "Téléphone est vide!")
		elif not telephone.isdigit():
			self.add_error("telephone", "Téléphone est incorrect!")
		adresse=self.data['adresse']
		if not adresse:
			self.add_error("adresse", "Address est vide!")

		return super(Profile, self).is_valid()

	def enregistrer(self, pseudo):
		nom=self.cleaned_data['nom']
		prenom=self.cleaned_data['prenom']
		telephone=self.cleaned_data['telephone']
		adresse=self.cleaned_data['adresse']

		Utilisateur.update(pseudo=pseudo, nom=nom, prenom=prenom, telephone=telephone, adresse=adresse)
