from mysite.settings import STATIC_URL
from django.db.models.functions import Coalesce
from django.core.serializers import serialize
from django.db.models import Avg
import hashlib
import urllib
import json
import os

def to_float(string):
	try:
		return float(string)
	except ValueError:
		return None


TYPE_PROJET=[
	#("O", "OpenWeather"),
	("N", "Parcelle et OpenWeather"),
        #("P", "Plante")
	
]

def mot_de_passe_hash(valeur):
	mot_de_passe_hash=hashlib.md5()
	mot_de_passe_hash.update(valeur.encode('utf-8'))
	return mot_de_passe_hash.hexdigest()


def as_geojson(queryset):
	return serialize('geojson', queryset)

def get_altitude(latitude, longitude):
	apikey="AIzaSyDB__9ljeKo2BWkqUv6mahxdIbDgSI8qmY"
	url="https://maps.googleapis.com/maps/api/elevation/json"
	request=urllib.urlopen(url+"?locations="+str(latitude)+","+str(longitude)+"&key="+apikey)
	try:
		results=json.load(request).get('results')
		if 0<len(results):
			altitude=results[0].get('elevation')
			return altitude
		else:
			print ('HTTP GET Request a echoue.')
	except ValueError:
		print ('JSON decode a echoue: '+str(request))
	return None
