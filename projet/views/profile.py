from projet.forms.profile import Profile
from django.http import HttpResponseRedirect, JsonResponse
from projet.forms.mot_de_passe import Mdp
from projet.models import Utilisateur
from django.shortcuts import render
from hashlib import md5

def index(request, formulaire=None):
	pseudo=request.session['pseudo']
	utilisateur=Utilisateur.objects.get(pseudo=pseudo)
	
	if not formulaire:
		data={}
		data['nom']=utilisateur.nom
		data['prenom']=utilisateur.prenom
		data['email']=utilisateur.email
		data['adresse']=utilisateur.adresse
		data['telephone']=utilisateur.telephone
		data['pseudo']=utilisateur.pseudo
		formulaire=Profile(data)
	return render(request, 'projet/profile.html', {'pseudo': pseudo, 'form': formulaire})

def valider(request):
	if request.method=='POST':
		formulaire=Profile(request.POST, request.FILES)
		pseudo=request.session['pseudo']
		if formulaire.is_valid():
			formulaire.enregistrer(pseudo=pseudo)
			return HttpResponseRedirect('/projet/mes-projets/')
		return index(request=request, formulaire=formulaire)
	return HttpResponseRedirect('/projet/mon-profile/')



def mot_de_passe(request, formulaire=None):
	pseudo=request.session['pseudo']
	if not formulaire:
		formulaire=Mdp({})
	return render(request, 'projet/mot_de_passe.html', {'pseudo': pseudo, 'form' : formulaire})

def valider_mot_de_passe(request):
	if request.method=='POST':
		pseudo=request.session['pseudo']
		formulaire=Mdp(request.POST)
		if formulaire.is_valid(pseudo=pseudo):
			request.session['mot_de_passe']=formulaire.enregistrer(pseudo=pseudo)
			return HttpResponseRedirect('/projet/mes-projets/')
		return mot_de_passe(request=request, formulaire=formulaire)
	return HttpResponseRedirect('/projet/profile/mot-de-passe/')
