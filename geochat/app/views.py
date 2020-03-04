from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout, login, authenticate
from .models import *
from .forms import *

def chat(request):
    context = {}
    if request.method == "POST":
        form = RegisterForm(request.POST)
        context['form'] = form
        if not request.user.is_authenticated:
            if form.is_valid():
                user = form.save(commit=False)
                user.email = form.data['email']
                user.save()
                return render(request, 'chat.html', context)
            else:
                username = request.POST['username_auth']
                password = request.POST['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect("/chat")
        else:
            text = request.POST.get('message')
            if text == '':
                return HttpResponseRedirect("/chat")
            new_message = Message()
            new_message.text = text
            new_message.author = request.user
            new_message.save()
            return HttpResponseRedirect("/chat")
    if request.method == "GET":
        context['messages'] = Message.objects.all()
        return render(request,"chat.html",context)

def index(request):
    return render(request,'index.html')