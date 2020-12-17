from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
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
            return redirect('staff_home')

        elif user.groups.filter(name__exact='passengers').exists():
            nex = request.session.get('next')
            print(nex)
            return redirect(nex)
    else:
        context['message'] = 'Incorrect Username or Password!'
        return render(request, 'login.html', context)


@unauthenticated_user
def login_get(request):
    context = {

    }
    request.session['next'] = request.GET.get('next', '/')
    return render(request, 'login.html', context)


def logout_view(request):
    logout(request)
    return redirect('index')
