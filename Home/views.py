from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from Users.models import User
from django.contrib.auth.models import Permission
from Posts.models import Event


def home(request):
    events = Event.objects.filter(active=True)
    data = {
        'events': events
    }

    return render(request, 'Home/index.html', data)


def page_not_found_404(request, exception):
    return render(request, 'Home/page_404.html')
