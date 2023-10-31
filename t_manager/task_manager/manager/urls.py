from django.urls import path
from .views import *

urlpatterns = [
    path('', MainView.as_view(), name='home'),
    path('tasks/<slug:task_slug>/', TaskView.as_view(), name='task_view'),
    path('fav-tasks/', FavTaskView.as_view(), name='fav_tasks'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('task/<int:task_id>', add_fav, name='add_fav'),
    path('create-task/', CreateTask.as_view(), name='add_task'),
    path('complete-task/<int:task_id>', complete_task, name='complete'),
    path('delete/<int:task_id>', delete_task, name='delete'),
    path('search/', search, name='search')
]
