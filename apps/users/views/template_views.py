from django.shortcuts import render

def login_page(request):
    return render(request, "login.html")

def index_page(request):
    return render(request, "index.html")
