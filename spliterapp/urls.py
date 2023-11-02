from django.urls import path
from . import views

urlpatterns = [
    path('main/', views.main, name='main'),
    path('create_group/', views.create_group, name='create_group'),
    path('group/<int:group_id>/', views.group_detail, name='group_detail'),
]
