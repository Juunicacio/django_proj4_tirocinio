from django.shortcuts import render

def full_thesis(request):
    return render(request, 'thesis/full_thesis.html')
