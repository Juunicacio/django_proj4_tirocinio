from django.shortcuts import render

def home(request):
    return render(request, 'dashboard/index.html')

def dashboard_graphs(request):
    return render(request, 'dashboard/dashboard_graphs.html')
