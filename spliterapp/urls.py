from django.urls import path
from . import views
# app_name = "spliterapp"
urlpatterns = [
    # path('', views.index, name='index'),  # Home or landing page
    path('checkbox/', views.checkbox, name='checkbox'),  # Home or landing page
    path('create_group/', views.create_group, name='create_group'),
    path('group/<int:group_id>/', views.group_detail, name='group_detail'),
    path('add_expense/<int:group_id>/', views.add_expense, name='add_expense'),
    path('delete_group/<int:group_id>/', views.delete_group, name='delete_group'),
    path('expense_detail/<int:expense_id>/', views.expense_detail, name='expense_detail'),
    #  path('detailed_repayments/<int:group_id>/<int:user_id>/',views.detailed_repayments, name='detailed_repayments'),
    # #  path('group/<int:group_id>/user/<int:user_id>/suggested-repayments/', views.suggested_repayments, name='suggested_repayments'),
    path('group/<int:group_id>/<int:user_id>/detailed-repayments/', views.detailed_repayments, name='detailed_repayments'),

]