from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Subtask, Task
from ..serializers import TaskSerializer,SubtaskSerializer
from django.db.models.signals import post_save
from django.dispatch import receiver,Signal

custom_signal=Signal()

@receiver(custom_signal)
def show_notification(sender, **kwargs):
    print(sender)
    print(kwargs['instance'].task.subtasks)
    print("Notification")

@receiver(post_save,sender=Subtask)
def update_percentage(sender,instance,**kwargs): 
    task=instance.task
    task.percentage=(task.subtasks.filter(complete=True).count()/task.subtasks.count())*100
    task.save()


class TaskListApiView(APIView):
    def get(self,request,*args, **kwargs):
        users=Task.objects.all()
        serializer=TaskSerializer(users,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        subtask_list=request.data.get('subtasks')
        data={
            'title':request.data.get('title'),
            'user':request.data.get('user')
        }
        serializer=TaskSerializer(data=data)
        if serializer.is_valid():
            task_instance=serializer.save()
            for subtask in subtask_list:
                data={
                    'title':subtask,
                    'task':task_instance.id # type: ignore
                }
                sub_serializer=SubtaskSerializer(data=data)
                if sub_serializer.is_valid():
                    sub_serializer.save()
                else:
                    task_instance.delete() # type: ignore
                    return Response(sub_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetailApiView(APIView):
    def get_object(self,task_id):
        try:
            return Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return None

    def get(self,request,task_id,*args, **kwargs):
        task_instance=self.get_object(task_id)
        if not task_instance:
            return Response(
                {"res":"Object not found with id {}".format(task_id)}
            )
        serializer=TaskSerializer(task_instance)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,task_id,*args, **kwargs):
        task_instance=self.get_object(task_id)
        if not task_instance:
            return Response(
                {"res":"Object not found with id {}".format(task_id)}
            )
        data={
            'title':request.data.get('title'),
            'user':task_instance.user
        }
        serializer=TaskSerializer(instance=task_instance,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, task_id, *args, **kwargs):
        task_instance=self.get_object(task_id)
        if not task_instance:
            return Response(
                {"res":"Object not found with id {}".format(task_id)}
            )
        
        task_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )