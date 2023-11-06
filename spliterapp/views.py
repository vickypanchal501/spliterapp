from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Group
from account.models import CustomUser



def create_group(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        creator = request.user
        group = Group.objects.create(name=group_name, creator=creator)
        group.members.add(creator)
        group.save()
        return redirect('group_detail', group_id=group.id)
    return render(request, 'group/main.html')

def group_detail(request, group_id):
    group = Group.objects.get(id=group_id)
    user = request.user  # Get the current user
    user_groups = Group.objects.filter(members=user)


    if request.method == 'POST':
        invited_user_username = request.POST.get('invited_user')
        try:
            invited_user = CustomUser.objects.get(username=invited_user_username)
            group.members.add(invited_user)
            return redirect('group_detail', group_id=group.id)
        except CustomUser.DoesNotExist:
            # Handle the case where the user doesn't exist
            pass
        
    return render(request, 'group/main.html', {'group': group,'user_groups': user_groups, 'user_id': user })

# def group_list(request):
#     user = request.user  # Get the current user
#     user_groups = Group.objects.filter(members=user)
#     return render(request, 'group/main.html', {})