from django.conf.urls import url
from .views.acceuil import index as acceuil, connexion, valider as valider_connexion, deconnexion, envoyer_message
from .views.inscription import index as formulaire_inscription, valider as valider_inscription
from .views.profile import index as formulaire_profile, valider as valider_profile, mot_de_passe, valider_mot_de_passe
from .views.projet import index as mes_projets, creation_projet, valider_projet, projet
from .views.parcelle import index as creation_parcelle, importer_polygone, valider_parcelle
from .views.noeud import index as noeud, valider_noeud
#from .views.polygon import index, savePolygons
#from projet import views

urlpatterns = [
             url(r'^$', acceuil, name='acceuil'),
             url(r'^envoyer-message/$', envoyer_message, name='envoyer_message'),
             url(r'^connexion/$', connexion, name='connexion'),
             url(r'^connexion/validation/$', valider_connexion, name='valider_connexion'),
             url(r'^deconnexion/$', deconnexion, name='deconnexion'), 
             url(r'^inscription/$', formulaire_inscription, name='inscription'),
             url(r'^inscription/validation/$', valider_inscription, name='valider_inscription'),
             url(r'^profile/$', formulaire_profile, name='profile'),
             url(r'^profile/validation/$', valider_profile, name='valider_profile'),
             url(r'^profile/mot-de-passe/$', mot_de_passe, name='changer_mot_de_passe'),
             url(r'^profile/mot-de-passe/validation/$', valider_mot_de_passe, name='valider_mot_de_passe'),
             url(r'^mes-projets/$', mes_projets, name='mes_projets'),
             url(r'^creation-projet/$', creation_projet, name='creation_projet'),
             url(r'^creation-projet/validation/$', valider_projet, name='valider_projet'),
             url(r'^mes-projets/(?P<projet>\d+)/$', projet, name='projet'),
             url(r'^importer-polygone/$', importer_polygone, name='importer_polygone'),
             url(r'^(?P<projet>\d+)/parcelle/$', creation_parcelle, name='creation_parcelle'),
             url(r'^(?P<projet>\d+)/parcelle/validation/$', valider_parcelle, name='valider_parcelle'),
             url(r'^(?P<projet>\d+)/noeud/$', noeud, name='noeud'),
             url(r'^(?P<projet>\d+)/noeud/validation/$', valider_noeud, name='valider_noeud'),
                    
            #url(r'^index/$', index , name ='index'),
            #url(r'^savepolygon/$', savePolygons, name = 'savepolygons'),
                       
]
