from django.urls import path
from .views import (task_list,
                    task_create,
                    task_update,
                    task_delete,
                    login_user,
                    logout_user,
                    register_user,)

urlpatterns = [
    path('', task_list, name ='task_list'),
    path('task/update/<int:pk>/', task_update, name ='task_update'),
    path('task/delete/<int:pk>/', task_delete, name ='task_delete'),
    path('task/create/', task_create, name ='task_create'),
    path('login_user/', login_user, name ='login_user'),
    path('logout_user/', logout_user, name ='logout_user'),
    path('register_user/', register_user, name ='register_user'),
]
