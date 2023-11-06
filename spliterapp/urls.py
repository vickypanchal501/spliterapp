from django.urls import path
from . import views
# app_name = "spliterapp"
urlpatterns = [
    # path('main/', views.main, name='main'),
    path('create_group/', views.create_group, name='create_group'),
    path('group/<int:group_id>/z', views.group_detail, name='group_detail'),
]
