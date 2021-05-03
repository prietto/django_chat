from django.conf.urls import url
from django.contrib import admin
from chat.views import *
from django.urls import path
from django.contrib.auth.views import LogoutView
from chat.api import MessageAPI, UserAPI


urlpatterns = [
    path('', index, name='index'),
    path('user_register/', register, name='user_register'),
    path('chat/', chatRoom, name='chats'),
    path('api/create_message/', MessageAPI.as_view(), name='api_create_message'),
    path('api/delete_message/<int:record_id>/', MessageAPI.as_view(), name='api_delete_message'),
    path('api/messages/<str:user_sender>/', MessageAPI.as_view(), name='api_message_list'),
    path('api/create_user/', UserAPI.as_view(), name='api_create_user'),
    path('logout/', LogoutView.as_view(), {'next_page': 'index'}, name='logout'),
    path('upload_img/', upload_img,  name='upload_img'),
    
    
]


if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    from django.views.static import serve
    from django.conf import settings

    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
    ]
