from django.shortcuts import render

def basenav(request):
       
	return render(request, 'projet/baseNav.html', {})
