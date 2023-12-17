from django.contrib import admin
from django.urls import path, include
from TodoAPI import urls as todo_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(todo_urls))
]
