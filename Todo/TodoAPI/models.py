from django.db import models
from django.utils import timezone
from django.db.models import JSONField

class UserProfile(models.Model):
    name=models.CharField(max_length=255, blank=False)
    email=models.EmailField()
    created_at=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{}'.format(self.name)

class Subtask(models.Model):
    title = models.CharField(max_length=255, blank=False)
    complete = models.BooleanField(default=False)
    task = models.ForeignKey('Task', related_name='subtasks', on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.title)
    

class Task(models.Model):
    title = models.CharField(max_length=255,blank=False)
    percentage = models.IntegerField(default=0)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    # subtasks = JSONField(default=list)
    def __str__(self):
        return '{}'.format(self.title)