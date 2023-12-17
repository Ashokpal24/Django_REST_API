from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Subtask
from ..serializers import SubtaskSerializer
from .task_views import custom_signal

class SubtaskListApiView(APIView):
    def get(self,request,*args, **kwargs):
        users=Subtask.objects.all()
        serializer=SubtaskSerializer(users,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        data={
            'title':request.data.get('title'),
            'complete':request.data.get('complete'),
            'task':request.data.get('task')
        }
        serializer=SubtaskSerializer(data=data)
        if serializer.is_valid():
            
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SubtaskDetailApiView(APIView):
    def get_object(self,task_id):
        try:
            return Subtask.objects.get(id=task_id)
        except Subtask.DoesNotExist:
            return None

    def get(self,request,subtask_id,*args, **kwargs):
        subtask_instance=self.get_object(subtask_id)
        if not subtask_instance:
            return Response(
                {"res":"Object not found with id {}".format(subtask_id)}
            )
        serializer=SubtaskSerializer(subtask_instance)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,subtask_id,*args, **kwargs):

        subtask_instance=self.get_object(subtask_id)
        if not subtask_instance:
            return Response(
                {"res":"Object not found with id {}".format(subtask_id)}
            )
        data={
            'title':request.data.get('title'),
            'complete':request.data.get('complete'),
            'task':subtask_instance.task.id
        }
        serializer=SubtaskSerializer(instance=subtask_instance,data=data,partial=True)
        if serializer.is_valid():
            task_instance=serializer.save()
            custom_signal.send(sender=self,request=request,instance=task_instance)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, subtask_id, *args, **kwargs):
        subtask_instance=self.get_object(subtask_id)
        if not subtask_instance:
            return Response(
                {"res":"Object not found with id {}".format(subtask_id)}
            )
        
        subtask_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )