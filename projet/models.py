from django.db import models
from projet import   mot_de_passe_hash, TYPE_PROJET, to_float
from django.contrib.gis.db import models as gisModels
from django.contrib.gis.geos import GEOSGeometry, Point
from projet import get_altitude
import uuid
import os


# Create your models here.
class Utilisateur(gisModels.Model):
	nom=gisModels.CharField(max_length=20)
	prenom=gisModels.CharField(max_length=20)
	pseudo=gisModels.CharField(max_length=20, unique=True)
	mot_de_passe=gisModels.CharField(max_length=33)
	telephone=gisModels.IntegerField()
	email=gisModels.CharField(max_length=40)
	adresse=gisModels.CharField(max_length=50)
	position=gisModels.PointField(max_length=40, null=True)
	

	@classmethod
	def create(cls, nom, prenom, pseudo, mot_de_passe, telephone, adresse, email):
		#position=Point(to_float(longitude), to_float(latitude))
		utilisateur=cls(nom=nom, prenom=prenom, pseudo=pseudo, mot_de_passe=mot_de_passe, telephone=telephone,  email=email,   adresse=adresse)
		utilisateur.save()
		return utilisateur

	

	@classmethod
	def update(cls, pseudo, nom=None, prenom=None, mot_de_passe=None, telephone=None,  adresse=None, email=None):
		utilisateur=cls.objects.get(pseudo=pseudo)
		if mot_de_passe:
			utilisateur.mot_de_passe=mot_de_passe
		
		if nom:
			utilisateur.nom=nom
		if prenom:
			utilisateur.prenom=prenom
		if telephone:
			utilisateur.telephone=telephone
		if adresse:
			utilisateur.adresse=adresse
		#if latitude and longitude:
			#utilisateur.position=Point(to_float(longitude), to_float(latitude))
		if email:
			utilisateur.email=email
		utilisateur.save()
		return utilisateur

	@classmethod
	def exists(cls, pseudo, mot_de_passe):
		utilisateur=cls.objects.filter(pseudo=pseudo).first()
		if utilisateur:
			if mot_de_passe==mot_de_passe_hash(utilisateur.mot_de_passe):
				return utilisateur
		return None

	def __str__(self):
		return 'Utilisateur: %s %s, Pseudo: %s' % (self.nom, self.prenom, self.pseudo)

	class Meta:
		managed=True
		db_table='utilisateur'

class Polygone(gisModels.Model):
	polygone=gisModels.GeometryField(srid=4326)

	@classmethod
	def create(cls, geos_geometry):
		geometry=GEOSGeometry(geos_geometry.__str__())
		polygone=cls.objects.filter(polygone=geometry).first()
		if not polygone:
			polygone=cls(polygone=geometry)
			polygone.save()
		return polygone

	def __str__(self):
		return self.polygone.__str__()

	class Meta:
		managed=True
		db_table='polygone'



class Projet(models.Model):
	nom=models.CharField(max_length=50)
	date=models.DateTimeField(auto_now_add=True)
	utilisateur=models.ForeignKey(Utilisateur)
	#plante=models.ForeignKey(Plante, null=True, blank=True)
	polygone=models.ManyToManyField(Polygone)
	type=models.CharField(max_length=1, choices=TYPE_PROJET)

	@classmethod
	def create(cls, nom, pseudo, type):
		utilisateur=Utilisateur.objects.get(pseudo=pseudo)
		projet=cls(nom=nom, utilisateur=utilisateur, type=type)
		projet.save()
		return projet

	#@classmethod
	#def supprimer(cls, id):
	#	not_projet_all_polygones=list(cls.objects.filter(~Q(id=id)).distinct().values_list('polygone', flat=True))
	#	projet=cls.objects.get(id=id)
	#	polygones=projet.polygone.all()
	#	noeuds=Noeud.objects.filter(projet=projet)
	#	climats_noeuds=ClimatNoeud.objects.filter(noeud=noeuds)
	#	climats_open_weather=ClimatOpenWeather.objects.filter(projet=projet)
	#	climats_journalieres=ClimatJournaliere.objects.filter(projet=projet)
	#	for polygone in polygones:
	#		if not polygone.id in not_projet_all_polygones:
	#			polygone.delete()
	#	noeuds.delete()
	#	climats_noeuds.delete()
	#	climats_open_weather.delete()
	#	climats_journalieres.delete()
	#	projet.delete()

	@classmethod
	def add_polygones(cls, projet_id, geojson):
		projet=cls.objects.get(id=projet_id)
		features=geojson['features']
		for feature in features:
			geos_geometry=feature['geometry']
			polygone=Polygone.create(geos_geometry=geos_geometry)
			projet.polygone.add(polygone)

	def __str__(self):
		if (not self.polygone.exists()) or (not Noeud.objects.filter(projet=self.id).exists()):
			return 'PROJET INCOMPLET: %s' % self.nom
		return '[Date de Creation: %s]         %s' % (self.date.date().__str__(), self.nom)

	class Meta:
		managed=True
		db_table='projet'

class Noeud(gisModels.Model):
	identifiant_arduino=gisModels.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
	projet=models.ForeignKey(Projet)
	position=gisModels.PointField()
	altitude=gisModels.FloatField()
	temperature=gisModels.BooleanField()
	#humidite=gisModels.BooleanField()
	#vent=gisModels.BooleanField()
	radiation=gisModels.BooleanField()
	humidite_sol=gisModels.BooleanField()

	@classmethod
	def create(cls, geojson, projet):
		features=geojson['features']
		projet=Projet.objects.get(id=projet)
		for feature in features:
			geos_geometry=feature['geometry']
			latitude=geos_geometry['coordinates'][0][0][0]
			longitude=geos_geometry['coordinates'][0][0][1]
			altitude=get_altitude(latitude=latitude, longitude=longitude)
			if altitude:
				position=Point(to_float(longitude), to_float(latitude))
				properties=feature['properties']
				temperature=properties['temperature ']
				#humidite=temperature
				#vent=properties['vent']
				radiation=properties['radiation solaire']
				humidite_sol=properties['humidite de sol']
				noeud=cls(projet=projet, position=position, temperature=temperature,  radiation=radiation, humidite_sol=humidite_sol, altitude=altitude)
				noeud.save()

	def __str__(self):
		return self.identifiant_arduino.__str__()

	class Meta:
		managed=True
		db_table='noeud'






#class User(models.Model):
 #   username = models.CharField(max_length=200)

  #  def __str__(self):
   #     return self.username


#class Polygon(models.Model):
#   user = models.ForeignKey(User)
#    points = models.CharField(max_length=500)

#    def __str__(self):
#        return self.user.username + " " + self.points

#    def get_points_list_to_json(self):
#        polygon_dict = {}
#        polygon_dict['username'] = self.user.username
#        polygon_dict['locations'] = [{'lat': pair[0], 'lng': pair[1]} for pair in ast.literal_eval(self.points)]
#        return json.dumps(polygon_dict)


       



