from django.urls import path, include
from .views.user_views import (
    hello_world,
    UserListApiView,
    UserDetailApiView   
)
from .views.task_views import (
    TaskListApiView,
    TaskDetailApiView
)

from .views.subtask_views import(
    SubtaskListApiView,
    SubtaskDetailApiView
)

urlpatterns = [
    path('', hello_world,name="Hello"),
    path('api/', UserListApiView.as_view()),
    path('api/<int:user_id>', UserDetailApiView.as_view()),
    path('api/task/',TaskListApiView.as_view()),
    path('api/task/<int:task_id>',TaskDetailApiView.as_view()),
    path('api/subtask/',SubtaskListApiView.as_view()),
    path('api/subtask/<int:subtask_id>',SubtaskDetailApiView.as_view()),
]