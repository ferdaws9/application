from django.shortcuts import render
from projet.models import User, Polygon
import json
from django.http import HttpResponse


# Create your views here.

def index(request):

    query = User.objects.filter(username__exact=request.user.username)

    if query is None or len(query) < 1:
        User(username=request.user.username).save()

    context = {'username': request.user.username}
    return render(request, 'projet/test.html', context)



def savePolygons(request):
    if request.method == 'POST':
        data = request.POST
        user = User.objects.filter(username__exact=request.user.username)
        if not user is None and len(user) > 0:
            points = []
            for i in range(len(data)):
                if not data.get('data['+str(i)+'][lat]') is None:
                    points.append((float(str(data.get('data['+str(i)+'][lat]'))), float(str(data.get('data['+str(i)+'][lng]')))))
            Polygon(user=user[0], points=str(points)).save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)
