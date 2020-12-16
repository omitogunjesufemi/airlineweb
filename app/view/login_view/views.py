from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from app.decorators import unauthenticated_user


@unauthenticated_user
def login_page_post(request):
    context = {

    }
    username = request.POST['username']
    password = request.POST['password']
    user: User = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        if user.groups.filter(name__exact='staffs').exists():
            return redirect('')

        elif user.groups.filter(name__exact='passengers'):
            return redirect('')
    else:
        context['message'] = 'Incorrect Username or Password!'
        return render(request, 'login.html', context)


@unauthenticated_user
def login_get(request):
    context = {

    }
    return render(request, 'login.html', context)
