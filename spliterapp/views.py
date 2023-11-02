from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Group
from account.models import CustomUser

def main(request):
    return render(request, "group/main.html")

def create_group(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        creator = request.user
        group = Group.objects.create(name=group_name, creator=creator)
        group.members.add(creator)
        group.save()
        return redirect('group_detail', group_id=group.id)
    return render(request, 'group/create_group.html')

def group_detail(request, group_id):
    group = Group.objects.get(id=group_id)
    if request.method == 'POST':
        invited_user_username = request.POST.get('invited_user')
        try:
            invited_user = CustomUser.objects.get(username=invited_user_username)
            group.members.add(invited_user)
            return redirect('group_detail', group_id=group.id)
        except CustomUser.DoesNotExist:
            # Handle the case where the user doesn't exist
            pass
    return render(request, 'group/group_detail.html', {'group': group})
