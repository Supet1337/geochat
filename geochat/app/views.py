from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.hashers import check_password
from .models import *
from .forms import *
import json

def ajax_circle(request):
    print(request.is_ajax)
    if request.is_ajax:
        new_circle = Circle()
        new_circle.x = request.POST.get('x')
        new_circle.y = request.POST.get('y')
        new_circle.save()
    return HttpResponseRedirect('/')

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

def ajax_circle_draw(request):

    circles = []
    for circle in Circle.objects.all():
        circles.append(circle.json())
    print(circles)
    return HttpResponse(json.dumps(circles))

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
        room = Room.objects.get(id=number)
        joins = JoinRoom.objects.filter(room_id=number)
        for join in joins:
            if request.user == join.user:
                context['room'] = room
                join_rooms = JoinRoom.objects.filter(user=request.user)
                rooms = []
                for join_room in join_rooms:
                    rooms.append(Room.objects.get(id=join_room.room_id))
                context['rooms'] = rooms
                return render(request,"mess.html",context)
        if room.is_private:
            return HttpResponse('У вас нет доступа к этому чату')
        else:
            new_join = JoinRoom()
            new_join.user = request.user
            new_join.room_id = number
            new_join.save()
            context['room'] = room
            join_rooms = JoinRoom.objects.filter(user=request.user)
            rooms = []
            for join_room in join_rooms:
                rooms.append(Room.objects.get(id=join_room.room_id))
            context['rooms'] = rooms
            return render(request, "mess.html", context)

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
        return HttpResponseRedirect('/')
    if request.method == "GET":
        return render(request,'create-room.html')


def rooms(request):
    if request.method == 'POST':
        room_enter = Room.objects.get(id=request.POST.get('id'))
        if check_password(request.POST.get('password'),room_enter.password):
            new_join = JoinRoom()
            new_join.user = request.user
            new_join.room_id = request.POST.get('id')
            new_join.save()
            return HttpResponseRedirect('/room/' + str(request.POST.get('id')))
        else:
            return HttpResponse('Неправильный пароль')
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
        else:
            if request.POST.get('name') == None:
                room_enter = Room.objects.get(id=request.POST.get('id'))
                if check_password(request.POST.get('password'), room_enter.password):
                    new_join = JoinRoom()
                    new_join.user = request.user
                    new_join.room_id = request.POST.get('id')
                    new_join.save()
                    return HttpResponseRedirect('/room/' + str(request.POST.get('id')))
                else:
                    return HttpResponse('Неправильный пароль')
            else:
                new_room = Room()
                new_room.author = request.user
                new_room.name = request.POST.get('name')
                new_room.password = request.POST.get('password')
                if request.POST.get('is_private'):
                    new_room.is_private = True
                else:
                    new_room.is_private = False
                new_room.save()
                return HttpResponseRedirect('/')



    if request.method == "GET":
        join_rooms = []
        if request.user.is_authenticated:
            join_rooms = JoinRoom.objects.filter(user=request.user)

        roomsj = []
        for join_room in join_rooms:
            roomsj.append(Room.objects.get(id=join_room.room_id))
        context['roomsj'] = roomsj
        rooms = []
        flag = False
        for room in Room.objects.all():
            for roomj in roomsj:
                if room == roomj:
                    flag = True
                    break
            if not flag:
                rooms.append(room)
            flag = False
        context['rooms'] = rooms
        return render(request,'index.html',context)

def profile(request, number):
    context = {}
    user = User.objects.get(id=number)
    context['username'] = user.username
    context['email'] = user.email
    context['last_login'] = user.last_login
    context['room'] = room

    join_rooms = JoinRoom.objects.filter(user=request.user)
    rooms = []
    for join_room in join_rooms:
        rooms.append(Room.objects.get(id=join_room.room_id))
    context['rooms'] = rooms

    return render(request,'profile.html', context)