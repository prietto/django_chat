# django_chat
Sitio Demo Online => http://chatapp-django.herokuapp.com/

Aplicacion Chat Realizada con Django Channels 1.1.8

Se permite la creacion de registros por medio de API

Crear Mensaje => /api/create_mensaje/ Metodo POST. body = { "sender_user": "pepito", "message":"Espero todo este cool!" }

Consultar Mensajes => /api/messages/str:user_sender/ Metodo GET parametro <user_sender> es opcional de no enviarlo, retorna todos los mensajes

Eliminar Mensaje => /api/delete_message/int:record_id/ Metodo DELETE parametro record_id es obligatorio

Creacion de Usuario => /api/create_user/ Metodo: POST {
"username":"juanita", "password": "s1st3m4s" }

SUPER USUARIO: user: admin pass: DeV.2021