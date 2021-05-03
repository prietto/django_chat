from rest_framework.views import APIView
from chat.serializers import MessageSerializers, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from chat.models import Message
from django.contrib.auth.models import User
from django.http import Http404

class MessageAPI(APIView):

    def get_object(self, record_id):
        try:
            return Message.objects.get(id=record_id)
        except Message.DoesNotExist:
            raise Http404

    def post(self, request):
        serializer = MessageSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def get(self, request, user_sender=None):
        try:
            if user_sender:
                user_obj = User.objects.filter(username=str(user_sender)).first()
                if user_obj:                
                    messages = Message.objects.filter(sender_user_id=user_obj.id)
            else:
                messages = Message.objects.filter().order_by('creation_date')
                
            serializer = MessageSerializers(messages, many=True, context={'request': request})      
            return Response(serializer.data, status=200)
        except Exception as err:
            print(str(err))

            return Response(status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, record_id=None):
        if record_id:
            message = self.get_object(record_id)
            message.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise Http404

        

class UserAPI(APIView):
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




        
    

