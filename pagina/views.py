from django.shortcuts import render

# Create your views here.
def index(request):

    return render(request, 'pagina/index.html')

def about(request):

    return render(request, 'pagina/about.html')

def client(request):

    return render(request, 'pagina/client.html')

