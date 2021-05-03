from rest_framework import serializers
from chat.models import Message
from django.contrib.auth.models import User

class UserSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    username = serializers.CharField()
    password = serializers.CharField()

    def create(self, validate_data):
        instance = User()
        instance.username = validate_data.get('username')        
        instance.set_password(validate_data.get('password'))
        instance.save()
        return instance
    
    def validate_username(self, data):
        users = User.objects.filter(username=data)
        if len(users)>0:
            raise serializers.ValidationError("El Usuario ya existe")
        else:
            return data
    
    class Meta:
        model= User
        fields = ['username','password']
    
    


class MessageSerializers(serializers.ModelSerializer):
    sender_user = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all(), many=False)
    message = serializers.CharField()

    #receiver_user = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all(), many=True)

    # def create(self, validate_data):
    #     instance = Message()
    #     instance.sender_user = validate_data.get('sender_user')
    #     instance.message = validate_data.get('message')
    #     instance.save()

    #     return instance

    class Meta:
        model= Message
        fields = ['id','sender_user','message','creation_date']

