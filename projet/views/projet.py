from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from projet.models import Projet, Utilisateur, Polygone, Noeud
from projet.forms.projet import Projet as CreationProjet
from .projet import Projet as Formulaire
from projet import as_geojson
#from ast import literal_eval

def index(request):
	pseudo=request.session['pseudo']
	projets=Projet.objects.filter(utilisateur__pseudo=pseudo)
	return render(request, 'projet/mes_projets.html', {'pseudo': pseudo, 'list': projets})

def projet(request, projet):
	projet=Projet.objects.get(utilisateur__pseudo=request.session['pseudo'], id=projet)
	if projet:
		noeuds=Noeud.objects.filter(projet=projet.id)
		polygones=projet.polygone.all()
		if  not polygones.exists():
			return HttpResponseRedirect('/projet/%d/parcelle/' % projet.id)
#		if not projet.plante:
#			return HttpResponseRedirect('/application/%d/choix-plante/' % projet.id)
#		if not projet.sol:
#			return HttpResponseRedirect('/application/%d/choix-sol/' % projet.id)
		if  not noeuds.exists():
			return HttpResponseRedirect('/projet/%d/noeud/' % projet.id)
		if polygones:
			centre=polygones.first().polygone.centroid
		else:
			centre=noeuds.first().position
		formulaire=Formulaire({'centre': centre, 'nom': projet.nom, 'date': projet.date, 'type': projet.type,  'noeuds': noeuds, 'parcelle': as_geojson(polygones.only('polygone')),  'noeud': as_geojson(noeuds), 'id': projet.id})
		formulaire.creer()
		pseudo=request.session['pseudo']
#		photo=utilisateurPhotoProfile(Utilisateur.objects.filter(pseudo=pseudo).first().photo)
		return render(request, 'projet/projet.html', {'projet': formulaire, 'pseudo': pseudo})
	return HttpResponseRedirect('/projet/mes-projets/')

def creation_projet(request):
	pseudo=request.session['pseudo']
	utilisateur=Utilisateur.objects.filter(pseudo=pseudo).first()
	return render(request, 'projet/creation_projet.html', {'form' : CreationProjet({}), 'pseudo': pseudo})

def valider_projet(request):
	if request.method=="POST":
		formulaire=CreationProjet(request.POST)
		pseudo=request.session['pseudo']
		if formulaire.is_valid():
			projet=formulaire.enregistrer(pseudo=pseudo)
			return HttpResponseRedirect('/projet/mes-projets/%d/' % projet.id)
		
		return render(request, "projet/creation_projet.html", {'form': formulaire, 'pseudo': pseudo})
	return HttpResponseRedirect('/projet/creation-projet/')

#def update_donnees(request, projet):
#	noeuds_non_actif, donnees=getDonnees(projet=Projet.objects.get(id=projet), graphes=literal_eval(request.POST['graphes']))
#	return JsonResponse({'graphe': noeuds_non_actif, 'donnee': donnees}, safe=False)

#def supprimer_projet(request, projet):
#	Projet.supprimer(id=projet)
#	return HttpResponseRedirect('/application/mes-projets/')
