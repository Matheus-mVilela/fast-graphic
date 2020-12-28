from django.shortcuts import render
from django.contrib.auth import logout


def logout_view(request):
    logout(request)
    return redirect('login.html')


# Create your views here.
