from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),
    # DM URLs
    path('dm/', views.dm_inbox, name='dm_inbox'),
    path('dm/<int:conversation_id>/', views.dm_conversation, name='dm_conversation'),
    path('dm/start/<str:username>/', views.start_dm, name='start_dm'),
    path('users/', views.user_list, name='user_list'),
    # group chat
    path('<slug:slug>/', views.room, name='room'),
]
