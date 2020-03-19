from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.hashers import check_password
from .models import *
from .forms import *
import json

@login_required
def ajax_send(request,number):
    if request.user.is_authenticated:
        print(request.is_ajax)
        if request.is_ajax:
            new_message = Message()
            text = request.POST.get('message')
            if not text == '':
                new_message.text = text
                new_message.author = request.user
                new_message.room = Room.objects.get(id=number)
                new_message.save()

    messages = []
    for message in Message.objects.filter(room_id=number):
        messages.append(message.json())
    print(messages)
    return HttpResponse(json.dumps(messages))

@login_required
def ajax_update(request,number):

    messages = []
    for message in Message.objects.filter(room_id=number):
        messages.append(message.json())
    print(messages)
    return HttpResponse(json.dumps(messages))

@login_required
def room(request,number):
    context = {}
    if request.method == "POST":
        text = request.POST.get('message')
        if text == '':
            return HttpResponseRedirect("/chat")
        new_message = Message()
        new_message.text = text
        new_message.author = request.user
        new_message.save()
        return HttpResponseRedirect("/chat")
    if request.method == "GET":
        context['messages'] = Message.objects.filter(room_id=number)
        context['room'] = Room.objects.get(id=number)
        return render(request,"chat.html",context)

@login_required
def create_room(request):
    if request.method == "POST":
        new_room = Room()
        new_room.author = request.user
        new_room.name = request.POST.get('name')
        new_room.password = request.POST.get('password')
        if request.POST.get('is_private'):
            new_room.is_private = True
        else:
            new_room.is_private = False
        new_room.save()
        return HttpResponseRedirect('rooms')
    if request.method == "GET":
        return render(request,'create-room.html')


def rooms(request):
    if request.method == 'POST':
        room_enter = Room.objects.get(id=request.POST.get('id'))
        if check_password(request.POST.get('password'),room_enter.password):
            return HttpResponseRedirect('/room/' + str(request.POST.get('id')))
        else:
            return HttpResponse('jopa')
    if request.method == 'GET':
        context = {}
        context['rooms'] = Room.objects.all()
        return render(request,'rooms.html',context)

def index(request):
    context = {}
    if request.method == "POST":
        form = RegisterForm(request.POST)
        context['form'] = form
        if not request.user.is_authenticated:
            if form.is_valid():
                user = form.save(commit=False)
                user.email = form.data['email']
                user.save()
                return render(request, 'index.html', context)
            else:
                username = request.POST['username_auth']
                password = request.POST['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect("/")
    if request.method == "GET":
        return render(request,'index.html')

