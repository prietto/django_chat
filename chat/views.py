# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from chat.serializers import UserSerializer, MessageSerializers
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from django.http.response import HttpResponse
import json
from chat.forms import LoginForm
from django.contrib.auth.models import User
from chat.models import Message
import datetime
import os
import hashlib
import random
from django.conf import settings


def index(request):

    if request.user.is_authenticated:
        return redirect('chats')
    
    if request.method == 'GET':
        return render(request, 'chat/index.html')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
        
        else:
            context = {'error':'Usuario no Existe'}
            return render(request, 'chat/index.html',context)
            #return HttpResponse(json.dumps(result))
            
        
        return redirect('chats')



def chatRoom(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        template = 'chat/chat_room.html'

        m_list = Message.objects.filter().order_by('creation_date')
        result = []
        for msg in m_list:
            row = {
                "id": msg.id,
                "sender_user": msg.sender_user.username,
                "sender_user_id": str(msg.sender_user.id),
                "message":msg.message,
                "creation_date": datetime.datetime.strftime(msg.creation_date, '%Y-%m-%d')
            }
            result.append(row)

        ctx = {
            'users': User.objects.exclude(username=request.user.username),
            'messages': json.dumps(result)
        }
        return render(request, template,ctx)


def register(request):

    if request.method == 'POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('chats')        

    else:
        form= LoginForm()

    context = {
        'form': form
    }
    return render(request, 'chat/user_register.html', context)




def upload_img(request):
    result = {"status":True, "mensaje":"Imagen guardada"}
    try:
        if request and hasattr(request,"FILES") and 'imagen' in request.FILES:
            image = request.FILES.get("imagen")
            allow_ext = ["png", "jpeg", "jpg", "gif", "webm"]
            extension = os.path.splitext(image.name)[1][1:]
            if extension.lower() in allow_ext:

                guid = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()
                image_name = "{}.{}".format(guid, extension)

                if not os.path.exists(settings.UPLOADS_ROOT):
                    os.makedirs(settings.UPLOADS_ROOT)

                file_path = os.path.join(settings.UPLOADS_ROOT, image_name)
                with open(file_path, 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)
                result["url"] = '/media/uploads/{}'.format(image_name)
            else:
                result["status"] = False
                result["mensaje"] = "El tipo de archivo es inválido"
        else:
            result["status"] = False
            result["mensaje"] = "No se envió ningún archivo"
    except Exception as err:
        result["status"] = False
        result["mensaje"] = "Ocurrió un error"
        result["mensaje_error"] = str(err)

    
    return HttpResponse(json.dumps(result))
