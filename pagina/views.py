from django.shortcuts import render

# Create your views here.
def index(request):

    return render(request, 'pagina/index.html')

def about(request):

    return render(request, 'pagina/about.html')

def client(request):

    return render(request, 'pagina/client.html')

def log_in(request):

    return render(request, 'pagina/log_in.html')

def register(request):

    return render(request, 'pagina/register.html')
