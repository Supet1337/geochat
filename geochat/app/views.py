from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from .models import *
from .forms import *
import json


@login_required
def ajax_update_balance(request):
    wallet = Wallet.objects.get(user=request.user)
    wallet.balance += 1
    wallet.save()
    return HttpResponse(json.dumps({'balance': wallet.balance}))


@login_required
def ajax_load_messages(request, number):
    messages = []
    for message in Message.objects.filter(room_id=number):
        messages.append(message.json())
    return HttpResponse(json.dumps(messages))


@login_required
def ajax_maps_draw(request, number):
    rooms = []
    for room in Room.objects.filter(author_id=number):
        rooms.append(room.json())
    return HttpResponse(json.dumps(rooms))


@login_required
def ajax_circle_draw(request):
    join_rooms = []
    if request.user.is_authenticated:
        join_rooms = JoinRoom.objects.filter(user=request.user)

    roomsj = []
    for join_room in join_rooms:
        roomsj.append(Room.objects.get(id=join_room.room_id))
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
    rms = []
    for room in rooms:
        rms.append(room.json())
    return HttpResponse(json.dumps(rms))


@login_required
def ajax_circle_draw_joined(request):
    join_rooms = []
    if request.user.is_authenticated:
        join_rooms = JoinRoom.objects.filter(user=request.user)

    roomsj = []
    for join_room in join_rooms:
        roomsj.append(Room.objects.get(id=join_room.room_id))
    rms = []
    for room in roomsj:
        rms.append(room.json())
    return HttpResponse(json.dumps(rms))


@login_required
def room(request, number):
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
        try:
            context['image'] = Image.objects.get(user=request.user)
        except:
            context['image'] = -1
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
                return render(request, "mess.html", context)
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


def loggout(request):
    logout(request)
    return HttpResponseRedirect("/")


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
                new_Wallet = Wallet()
                new_Wallet.user = user
                new_Wallet.balance = 1000
                new_Wallet.save()
                login(request, user)

                message = 'Здравствуйте! {}\nПоздравляем! Вы успешно зарегестрировали аккаунт Geochat.\nВперёд к ' \
                          'новым приключениям!\n\n\n С уважением, команда Geochat  '.format(user.username)
                send_mail('Регистрация аккаунта Geochat', message, 'shp.geochat@gmail.com', [user.email],
                          fail_silently=False)
                return render(request, 'index.html', context)
            else:
                try:
                    username = request.POST['username_auth']
                    password = request.POST['password']
                except:
                    messages.error(request, 'Пароли не совпадают.')
                    return HttpResponseRedirect("/")
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect("/")
                else:
                    messages.error(request, 'Неправильный логин или пароль.')
                return HttpResponseRedirect("/")
        else:
            if request.POST.get('name') is None:
                room_enter = Room.objects.get(id=request.POST.get('id'))
                joins = JoinRoom.objects.filter(room_id=request.POST.get('id'))
                if len(joins) < room_enter.max_members:
                    if check_password(
                            request.POST.get('password'),
                            room_enter.password):
                        new_join = JoinRoom()
                        new_join.user = request.user
                        new_join.room_id = request.POST.get('id')
                        new_join.save()
                        return HttpResponseRedirect(
                            '/room/' + str(request.POST.get('id')))
                    else:
                        return HttpResponse('Неправильный пароль')
                else:
                    return HttpResponse(
                        'В данном чате уже максимальное количество пользователей')
            else:
                if not request.POST.get('name') == '':
                    new_room = Room()
                    wallet = Wallet.objects.get(user=request.user)
                    new_room.author = request.user
                    new_room.name = request.POST.get('name')
                    new_room.password = request.POST.get('password')
                    new_room.x = request.POST.get('x')
                    new_room.y = request.POST.get('y')
                    new_room.diametr = request.POST.get('choose_diametr')
                    new_room.max_members = request.POST.get('choose_max')
                    if request.POST.get('is_private'):
                        new_room.is_private = True
                    else:
                        new_room.is_private = False
                    if request.POST.get('is_place'):
                        new_room.is_place = True
                    else:
                        new_room.is_place = False
                    if wallet.balance - (int(new_room.diametr) - 50 + (int(new_room.max_members) - 3) * 10) >= 0:
                        wallet.balance -= int(new_room.diametr) - 50 + (int(new_room.max_members) - 3) * 10
                        wallet.save()
                    else:
                        return HttpResponse('Не хватает денег')
                    new_room.save()
                else:
                    return HttpResponse('Название не может быть пустым')
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
        if request.user.is_authenticated:
            context['balance'] = Wallet.objects.get(user=request.user).balance
        else:
            context['balance'] = 0
        try:
            context['image'] = Image.objects.get(user=request.user)
        except:
            context['image'] = -1
        return render(request, 'index.html', context)


def profile(request, number):
    if request.method == "POST":
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                image = Image.objects.get(user=request.user)
                image.delete()
            except:
                pass
            ava = form.save(commit=False)
            ava.user = request.user
            ava.save()
        return HttpResponseRedirect("../profile/" + str(number))
    form = UploadImageForm()
    context = {}
    user = User.objects.get(id=number)
    context['form'] = form
    try:
        context['image'] = Image.objects.get(user=user)
    except:
        context['image'] = -1
    context['username'] = user.username
    context['email'] = user.email
    context['last_login'] = user.last_login
    context['room'] = room
    context['id'] = number
    context['created_rooms'] = Room.objects.filter(author_id=number)
    context['balance'] = Wallet.objects.get(user_id=number).balance
    join_rooms = JoinRoom.objects.filter(user=request.user)
    rooms = []
    for join_room in join_rooms:
        rooms.append(Room.objects.get(id=join_room.room_id))
    context['rooms'] = rooms

    return render(request, 'profile.html', context)
