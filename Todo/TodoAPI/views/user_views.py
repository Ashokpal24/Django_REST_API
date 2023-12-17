from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import UserProfile
from ..serializers import UserSerializer

def hello_world(request):
    return HttpResponse("Hello world!")

class UserListApiView(APIView):
    def get(self,request,*args, **kwargs):
        users=UserProfile.objects.all()
        serializer=UserSerializer(users,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        data={
            'name':request.data.get('name'),
            'email':request.data.get('email')
        }
        serializer=UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserDetailApiView(APIView):
    def get_object(self,user_id):
        try:
            return UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return None

    def get(self,request,user_id,*args, **kwargs):
        user_instance=self.get_object(user_id)
        if not user_instance:
            return Response(
                {"res":"[GET] Object not found with id {}".format(user_id)},status=status.HTTP_404_NOT_FOUND
            )
        serializer=UserSerializer(user_instance)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,user_id,*args, **kwargs):
        user_instance=self.get_object(user_id)
        if not user_instance:
            return Response(
                {"res":"[PUT] Object not found with id {}".format(user_id)},status=status.HTTP_404_NOT_FOUND
            )
        data={
            'name':request.data.get('name'),
            'email':request.data.get('email')
        }
        serializer=UserSerializer(instance=user_instance,data=data,partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, user_id, *args, **kwargs):
        user_instance=self.get_object(user_id)
        if not user_instance:
            return Response(
                {"res":"{DEL] Object not found with id {}".format(user_id)}
            )
        
        user_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )