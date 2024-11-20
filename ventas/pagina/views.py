from django.shortcuts import render

# Create your views here.
def index(request):

    return render(request, 'index.html')

def about(request):

    return render(request, 'about.html')

def client(request):

    return render(request, 'client.html')

def log_in(request):

    return render(request, 'log_in.html')

def register(request):

    return render(request, 'register.html')
def adminpage(request):

    return render(request, 'adminpage.html')

def adminusuarios(request):

    return render(request, 'adminusuarios.html')

def inventarioadmin(request):

    return render(request, 'inventarioadmin.html')

def vendedor(request):

    return render(request, 'vendedor.html')

