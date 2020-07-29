from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.

def activity_log(request):
    return render(request, 'application/activity-log.html')

@login_required(login_url='login')
def player_database(request):
    return render(request, 'application/playerdatabase.html')

@login_required(login_url='login')
def afcon(request):
    return render(request, 'application/Afcon.html')

@login_required(login_url='login')
def caf(request):
    return render(request, 'application/Caf.html')

def profile_view(request):
    return render(request, 'application/profile.html')

def blank_view(request):
    return render(request, 'application/blank_page.html')