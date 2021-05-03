from channels import Group, Channel
from channels.sessions import channel_session
import json
from channels.auth import channel_session_user, channel_session_user_from_http
from chat.models import Message
from django.contrib.auth.models import User
import datetime

# Connected to chat-messages
def msg_consumer(message):
    # Save to model
    #room = message.content['room']
    
    data = json.loads(message.content['message'])
    username = data.get('username')
    msg = data.get('message')
    user = User.objects.filter(username=username).first()
    print('msg=> ',message.content)

    message_to_return = json.loads(message.content['message'])

    if data.get('action') == 'create':
        msg_obj = Message()
        msg_obj.sender_user = user
        msg_obj.message = msg
        msg_obj.save()
        message_to_return["id"] = msg_obj.id
        message_to_return["creation_date"] = datetime.datetime.strftime(msg_obj.creation_date, '%Y-%m-%d %H:%M:%S')
    
    if data.get('action') == 'delete':
        msg_obj = Message.objects.filter(id=data.get('id')).first()
        msg_obj.delete()
    
    # Broadcast to listening sockets
    message_to_return["action"] = data.get('action')
    
    Group('chat').send({
        'text':json.dumps(message_to_return)
    })

@channel_session_user_from_http
def ws_add(message):
    print('connection received')
    message.reply_channel.send({'accept':True})
    Group('chat').add(message.reply_channel)
    
    #Group("chat-%s" % message.user.username[0]).add(message.reply_channel)

@channel_session
def ws_message(message):
    print('Message Received')
    
    # Group('chat').send({
    #     'text':message.content['text']
    # })

    # Group("chat").send({
    #     "text": json.dumps({
    #         "text": message["text"],
    #         "username": message.channel_session["username"],
    #     }),
    # })
    Channel("chat-messages").send({
        "message": message['text'],
    })



    

def ws_disconnect(message):
    print('Connection Closed')
    Group('chat').discard(message.reply_channel)