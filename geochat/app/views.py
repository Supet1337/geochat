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

def find_joined_rooms(join_rooms, roomsj):
    '''
    Функция поиска чатов, в которые присоединился пользователь.

    :param join_rooms: Объекты JoinRoom
    :param roomsj: Массив
    :return: None
    '''
    for join_room in join_rooms:
        roomsj.append(Room.objects.get(id=join_room.room_id))

def room_sort(rooms, roomsj):
    '''
    Функция распределения чатов.

    :param rooms: Массив
    :param roomsj: Объекты Room
    :return: None
    '''
    flag = False
    for room in Room.objects.all():
        for roomj in roomsj:
            if room == roomj:
                flag = True
                break
        if not flag:
            rooms.append(room)
        flag = False

def find_image(context, user_add):
    '''
    Функция поиска аватара.

    :param context: Контекст
    :param user_add: Объект UserAdditionals
    :return: None
    '''
    if user_add.image == '':
        context['image'] = -1
    else:
        context['image'] = user_add.image

def doc(request):
    return render(request, "docs/build/html/index.html")

def view_404(request, exception):
    '''
Функция отображения ошибки 404.

    :param request: запрос
    :param exception: исключение
    :return: render 404.html
    '''
    return render(request, "errors/404.html")

def view_500(request):
    '''
    Функция отображения ошибки 500.

    :param request: запрос
    :return: render 500.html
    '''
    return render(request, "errors/500.html")



@login_required
def ajax_update_balance(request):
    '''
    Функция обновление баланса пользователя

    :param request: запрос
    :return: balance
    '''
    wallet = UserAdditionals.objects.get(user=request.user)
    wallet.balance += 1
    wallet.save()
    return HttpResponse(json.dumps({'balance': wallet.balance}))


@login_required
def ajax_load_messages(request, number):
    '''
    Функция загрузки сообщений

    :param request: запрос
    :param number: номер комнаты
    :return: messages
    '''
    messages = []
    for message in Message.objects.filter(room_id=number):
        messages.append(message.json())
    return HttpResponse(json.dumps(messages))


@login_required
def ajax_maps_draw(request,number):
    """
    Функция отрисовки карт в профиле через ajax

    :param request: запрос
    :param number: номер профиля
    :return: room
    """
    rooms = []
    for room in Room.objects.filter(author_id=number):
        rooms.append(room.json())
    return HttpResponse(json.dumps(rooms))


@login_required
def ajax_circle_draw(request):
    '''
    Функция отрисовки кругов через ajax

    :param request: запрос
    :return: rms
    '''
    join_rooms = []
    if request.user.is_authenticated:
        join_rooms = JoinRoom.objects.filter(user=request.user)

    roomsj = []
    find_joined_rooms(join_rooms,roomsj)
    rooms = []
    room_sort(rooms,roomsj)
    rms = []
    for room in rooms:
        rms.append(room.json())
    return HttpResponse(json.dumps(rms))


@login_required
def ajax_circle_draw_joined(request):
    '''
    Фукция отрисовки кругов через ajax, в которые пользователь уже вошёл

    :param request: запрос
    :return: rms
    '''
    join_rooms = []
    if request.user.is_authenticated:
        join_rooms = JoinRoom.objects.filter(user=request.user)

    roomsj = []
    find_joined_rooms(join_rooms, roomsj)
    rms = []
    for room in roomsj:
        rms.append(room.json())
    return HttpResponse(json.dumps(rms))


@login_required
def report(request):
    '''
    Функция репорта

    :param request: запрос
    :return: redirect "/"
    '''
    if request.method == "POST":
        report = Report()
        report.user = request.user
        report.report = request.POST.get('report')
        if report.report != '' and len(report.report) >= 10:
            report.save()
            messages.success(request, "Наши модераторы уже решают вашу проблему, простите за принесённые вам "
                                      "неудобства.")
        else:
            messages.error(request, "Собщение должно состоять не менее чем из 10 символов.")
        return HttpResponseRedirect("/")

@login_required
def room(request, number):
    """
    Функция рендера страницы mess.html

    :param request: запрос
    :param number: номер комнаты
    :type number: int
    :return: render mess.html
    """
    if len(JoinRoom.objects.filter(room_id=number,user=request.user)) == 0:
        messages.error(request, 'Вы пытаетесь войти в чат, в котором вы не находитесь,'
                                ' или такого чата уже не существует.')
        return HttpResponseRedirect("../../")
    else:
        context = {}
        form = RoomSettingsForm()
        context['form'] = form
        user_add = UserAdditionals.objects.get(user=request.user)
        context['my_balance'] = user_add.balance
        find_image(context, user_add)
        room = Room.objects.get(id=number)
        joins = JoinRoom.objects.filter(room_id=number)
        user_list = []
        for join in joins:
            user_list.append(UserAdditionals.objects.get(user=join.user))
        context['user_list'] = user_list
        for join in joins:
            if request.user == join.user:
                context['room'] = room
                join_rooms = JoinRoom.objects.filter(user=request.user)
                rooms = []
                find_joined_rooms(join_rooms,rooms)
                context['rooms'] = rooms
        return render(request, "mess.html", context)


def loggout(request):
    '''
    Функция деавторизации пользователя

    :param request: запрос
    :return: redirect на главную станицу
    '''
    logout(request)
    return HttpResponseRedirect("/")


def index(request):
    '''
    Функция рендера главной страницы

    :param request: запрос
    :return: render index.html
    '''
    context = {}
    join_rooms = []
    if request.user.is_authenticated:
        join_rooms = JoinRoom.objects.filter(user=request.user)

    roomsj = []
    find_joined_rooms(join_rooms,roomsj)
    context['roomsj'] = roomsj
    rooms = []
    room_sort(rooms, roomsj)
    context['rooms'] = rooms
    if request.user.is_authenticated:
        user_add = UserAdditionals.objects.get(user=request.user)
        context['balance'] = user_add.balance
        find_image(context,user_add)
    else:
        context['balance'] = 0
        context['image'] = -1

    return render(request, 'index.html', context)


@login_required
def profile(request, number):
    '''
    Функция рендера страницы профиля

    :param request: запрос
    :param number: номер профиля
    :type number: int
    :return: render profile.html
    '''
    context = {}
    user = User.objects.get(id=number)
    profile_user_add = UserAdditionals.objects.get(user=user)
    user_add = UserAdditionals.objects.get(user=request.user)
    find_image(context,profile_user_add)
    find_image(context,user_add)
    context['username'] = user.username
    context['email'] = user.email
    context['last_login'] = user.last_login
    context['room'] = room
    context['private_chats'] = profile_user_add.private_chats
    context['private_info'] = profile_user_add.private_info
    context['id'] = number
    context['status'] = profile_user_add.status
    context['created_rooms'] = Room.objects.filter(author_id=number)
    context['my_balance'] = user_add.balance
    join_rooms = JoinRoom.objects.filter(user=request.user)
    rooms = []
    find_joined_rooms(join_rooms, rooms)
    context['rooms'] = rooms
    if len(Room.objects.filter(author_id=number)) == 0:
        context['room_len'] = True


    return render(request, 'profile.html', context)




@login_required
def profile_settings(request):
    '''
    Функция рендера настроек профиля

    :param request: запрос
    :return: render profile_settings.html
    '''
    form = UserSettingsForm()
    context = {}
    context['form'] = form
    user_add = UserAdditionals.objects.get(user=request.user)
    find_image(context,user_add)
    context['username'] = request.user
    context['email'] = request.user.email
    context['last_login'] = request.user.last_login
    context['room'] = room
    context['id'] = request.user.id
    context['created_rooms'] = Room.objects.filter(author_id=request.user.id)
    context['my_balance'] = user_add.balance
    context['status'] = user_add.status
    if user_add.private_chats:
        context['private_chats'] = 'checked'
    if user_add.private_info:
        context['private_info'] = 'checked'
    join_rooms = JoinRoom.objects.filter(user=request.user)
    rooms = []
    find_joined_rooms(join_rooms, rooms)
    context['rooms'] = rooms
    return render(request,'profile_settings.html',context)

@login_required
def delete_room(request,number):
    '''
    Функция удаления комнаты.

    :param request: Запрос
    :param number: id комнаты
    :return: redirect to main page
    '''
    if request.method == "POST":
        Room.objects.get(id=number).delete()
        for join in JoinRoom.objects.filter(room_id=number):
            join.delete()
        return HttpResponseRedirect('../../')

def register_user(request):
    '''
    Функция регистрации пользователя.

    :param request: Запрос
    :return: redirect to main page
    '''
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.data['email']
            user_add = UserAdditionals()
            user_add.user = user
            user_add.balance = 1000
            if len(User.objects.filter(email=form.data['email'])) > 0:
                messages.error(request, "Пользователь с такой почтой уже существует.")
                return HttpResponseRedirect("../")
            elif len(User.objects.filter(username=form.data['username'])) > 0:
                messages.error(request, "Пользователь с таким ником уже существует.")
                return HttpResponseRedirect("/")
            elif check_password(request.POST.get('password1'),request.POST.get('password2')):
                messages.error(request, 'Пароли не совпадают.')
                return HttpResponseRedirect("/")
            else:
                user.save()
                user_add.save()
                login(request, user)
                message = 'Здравствуйте! {}\nПоздравляем! Вы успешно зарегестрировали аккаунт Geochat.\nВперёд к ' \
                          'новым приключениям!\n\n\n С уважением, команда Geochat  '.format(user.username)
                send_mail('Регистрация аккаунта Geochat', message, 'shp.geochat@yandex.ru', [user.email],
                          fail_silently=False)
        return HttpResponseRedirect('../')

def login_user(request):
    '''
    Функция логина пользователя.

    :param request: запрос
    :return: redirect to main page
    '''
    if request.method == "POST":
        username = request.POST['username_auth']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            messages.error(request, 'Неправильный логин или пароль.')
            return HttpResponseRedirect("/")

@login_required
def create_room(request):
    '''
    Функция создания чата.

    :param request: Запрос
    :return: redirect to main page
    '''
    if request.method == "POST":
        if not request.POST.get('name') == '':
            new_room = Room()
            wallet = UserAdditionals.objects.get(user=request.user)
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
                messages.error(request, "Вам не хватает монет для создания чата.")
                return HttpResponseRedirect('/')
            new_room.save()
            join_new_room = JoinRoom()
            join_new_room.user = request.user
            join_new_room.room_id = Room.objects.get(name=new_room.name).id
            join_new_room.save()
        else:
            messages.error(request, "Название чата не может быть пустым.")
        return HttpResponseRedirect('/')

@login_required
def join_room(request):
    '''
    Функция входа в чат.

    :param request: Запрос
    :return: redirect to room/room.id
    '''
    if request.method == "POST":
        room_enter = Room.objects.get(id=request.POST.get('id'))
        joins = JoinRoom.objects.filter(room_id=request.POST.get('id'))
        if len(joins) < room_enter.max_members:
            if room_enter.is_private:
                if check_password(request.POST.get('password'),room_enter.password):
                    new_join = JoinRoom()
                    new_join.user = request.user
                    new_join.room_id = request.POST.get('id')
                    new_join.save()
                    return HttpResponseRedirect('/room/' + str(request.POST.get('id')))
                else:
                    messages.error(request, "Неправильный пароль.")
                    return HttpResponseRedirect('/')
            else:
                new_join = JoinRoom()
                new_join.user = request.user
                new_join.room_id = request.POST.get('id')
                new_join.save()
                return HttpResponseRedirect('/room/' + str(request.POST.get('id')))
        else:
            messages.error(request, "В этом чате уже максимальное количество пользователей.")
            return HttpResponseRedirect('/')

@login_required
def update_profile_settings(request):
    '''
    Функция обновления настроек профиля.

    :param request: Запрос
    :return: redirect to /profile-settings
    '''
    if request.method == "POST":
        user_add = UserAdditionals.objects.get(user=request.user)
        user_add.status = request.POST.get('status')
        if request.POST.get('private_chats'):
            user_add.private_chats = True
        else:
            user_add.private_chats = False
        if request.POST.get('private_info'):
            user_add.private_info = True
        else:
            user_add.private_info = False
        user_add.save()
        messages.success(request, "Настройки успешно сохранены.")
        return HttpResponseRedirect("../profile-settings")

@login_required
def update_profile_picture(request):
    '''
    Функция обновления аватарки профиля.

    :param request: Запрос
    :return: redirect to /profile-settings
    '''
    if request.method == "POST":
        form = UserSettingsForm(request.POST, request.FILES)
        if form.is_valid():
            old_user_add = UserAdditionals.objects.get(user=request.user)
            user_add = form.save(commit=False)
            if user_add.image != "":
                try:
                    image = UserAdditionals.objects.get(user=request.user).image
                    image.delete()
                except:
                    pass
                old_user_add.image = user_add.image
                old_user_add.save()
                messages.success(request, "Аватарка успешно сохранена.")
            else:
                messages.error(request, "Выберите картинку.")
        else:
            messages.error(request, "Произошла ошибка.")
        return HttpResponseRedirect("../profile-settings")

@login_required
def update_room_picture(request,number):
    '''
    Функция обновления аватара чата.

    :param request: Запрос
    :param number: id чата
    :return: redirect to room/room.id
    '''
    if request.method == "POST":
        form = RoomSettingsForm(request.POST, request.FILES)
        if form.is_valid():
            old_room = Room.objects.get(id=number)
            new_room = form.save(commit=False)
            if new_room.image != "":
                try:
                    image = old_room.image
                    image.delete()
                except:
                    pass
                old_room.image = new_room.image
                old_room.save()
                messages.success(request, "Аватарка успешно изменена.")
            else:
                messages.error(request, "Выберите картинку.")
        else:
            messages.error(request, "Произошла ошибка.")
        return HttpResponseRedirect("../room/"+str(number))

@login_required
def update_room_settings(request,number):
    '''
    Функция обновления настроек чата.

    :param request: Запрос
    :param number: id чата
    :return: redirect to room/room.id
    '''
    if request.method == "POST":
        new_name = Room.objects.get(id=number)
        new_name.name = request.POST.get('name')
        new_name.save()
        messages.success(request, "Изменения успешно сохранены.")
        return HttpResponseRedirect("../room/" + str(number))

@login_required
def leave_chat(request, number):
    '''
    Функция выхода из чата.

    :param request: Запрос
    :param number: id чата
    :return: redirect to main page
    '''
    if request.method == "POST":
        us_id = request.POST.get('user-id')
        JoinRoom.objects.get(user_id=us_id, room_id=number).delete()
        if len(JoinRoom.objects.filter(room_id=number)) == 0:
            Room.objects.get(id=number).delete()
        if request.user.id != us_id:
            return HttpResponseRedirect("../room/" + str(number))
        else:
            return HttpResponseRedirect('../')
