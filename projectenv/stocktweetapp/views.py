from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
	return render(request, 'stocktweetapp/index.html')


def search_func(request):
	if request.method == "POST":
		searched = request.POST['searched']
		stocks = Stock.objects.filter(name__contains = searched)
		return render (request, 'templates/index.html', 
		{'searched':searched, 'stocks':stocks})
	else:
		 return render (request, 'templates/index.html', {})


	

