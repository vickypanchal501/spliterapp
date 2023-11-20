from django.urls import path
from . import views
# app_name = "spliterapp"
urlpatterns = [
    # path('', views.index, name='index'),  # Home or landing page
    path('checkbox/', views.checkbox, name='checkbox'),  # Home or landing page
    path('create_group/', views.create_group, name='create_group'),
    path('group/<int:group_id>/', views.group_detail, name='group_detail'),
    path('add_expense/<int:group_id>/', views.add_expense, name='add_expense'),
    

]