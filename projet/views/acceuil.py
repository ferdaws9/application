
from django.http import HttpResponseRedirect 
from projet.forms.connexion import Connexion
from projet.forms.contact import Email
from django.shortcuts import render

def index(request):
	return render(request, 'projet/acceuil.html', {'form': Email({})})


def connexion(request):
	return render(request, 'projet/connexion.html', {'form' : Connexion({})})

def valider(request):
	if request.method=='POST':
		connexion=Connexion(request.POST)
		if connexion.is_valid():
			request.session['pseudo']=connexion.get('pseudo')#est un dictionnaire pour stocker des informations entre les demandes.
			request.session['mot_de_passe']=connexion.get('mot_de_passe')
			return HttpResponseRedirect('/projet/mes-projets/')
		return render(request, 'projet/connexion.html', {'form' : connexion})
	return HttpResponseRedirect('/projet/connexion/')
def deconnexion(request):
	del request.session['pseudo']
	del request.session['mot_de_passe']
	return HttpResponseRedirect('/projet/')


def envoyer_message(request):
	if request.method=="POST":
		formulaire=Email(request.POST)
		if formulaire.is_valid():
			formulaire.envoyer_message()
		else:
			return render(request, 'acceuil.html', {'form': formulaire})
	return HttpResponseRedirect('/projet/')
