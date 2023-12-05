from django.urls import path
from . import views
# app_name = "spliterapp"
urlpatterns = [
<<<<<<< HEAD
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> vikas
=======
>>>>>>> vikcy
    # path('', views.index, name='index'),  # Home or landing page
    path('checkbox/', views.checkbox, name='checkbox'),  # Home or landing page
    path('create_group/', views.create_group, name='create_group'),
    path('group/<int:group_id>/', views.group_detail, name='group_detail'),
    path('add_expense/<int:group_id>/', views.add_expense, name='add_expense'),
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    
=======
    path('delete_group/<int:group_id>/', views.delete_group, name='delete_group'),
    path('expense_detail/<int:expense_id>/', views.expense_detail, name='expense_detail'),
    #  path('group/<int:group_id>/user/<int:user_id>/suggested-repayments/', views.suggested_repayments, name='suggested_repayments'),
    path('group/<int:group_id>/user/<int:user_id>/detailed-repayments/', views.detailed_repayments, name='detailed_repayments'),
>>>>>>> vicky

]
=======
<<<<<<< HEAD
    

]
=======
    
    # path('main/', views.main, name='main'),
    path('expense/', views.expense, name='expense'),
    path('create_group/', views.create_group, name='create_group'),
    path('group/<int:group_id>/z', views.group_detail, name='group_detail'),
]
>>>>>>> parent of dfdcf37 (this is commit today add expense in admin07/11/2023)
=======
]
>>>>>>> parent of 0701fcf (this is today commit enhance ui 08/11/20123)
>>>>>>> vikas
=======
    

]
>>>>>>> vikcy
