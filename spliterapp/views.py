from django.shortcuts import render, redirect
from .models import Group, Expense
from account.models import CustomUser
from .forms import ExpenseForm

def create_group(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        creator = request.user
        group = Group.objects.create(name=group_name, creator=creator)
        group.members.add(creator)
        group.save()
        return redirect('group_detail', group_id=group.id)
    return render(request, 'group/base.html')

def group_detail(request, group_id):
    group = Group.objects.get(id=group_id)
    user = request.user
    user_groups = Group.objects.filter(members=user)

    if request.method == 'POST':
        invited_user_username = request.POST.get('invited_user')
        try:
            invited_user = CustomUser.objects.get(username=invited_user_username)
            if invited_user not in group.members.all():
                group.members.add(invited_user)
            return redirect('group_detail', group_id=group.id)
        except CustomUser.DoesNotExist:
            # Handle the case where the user doesn't exist
            pass
          
    return render(request, 'group/base.html', {'group': group, 'user_groups': user_groups, 'user_id': user })


def add_expense(request, group_id):
    group = Group.objects.get(id=group_id)
    split_amount = 0 
    # import pdb; pdb.set_trace()
    if request.method == 'POST':
        form = ExpenseForm(group,request.POST)
        
        if form.is_valid():
            expense = form.save(commit=False)
            expense.created_by = request.user
            expense.group = group
            expense.save()

            # Calculate the split amount
            split_with_users = form.cleaned_data['split_with']
            split_amount = form.cleaned_data['split_amount']

            # Calculate the amount for each user
            amount_per_user = split_amount / (len(split_with_users) + 1)
            expense.split_amount = amount_per_user
            expense.save()

            # Add the creator to the split_with users
            split_with_users = list(split_with_users)
            split_with_users.append(request.user)
            expense.split_with.set(split_with_users)

            return redirect('group_detail', group_id=group.id)
    else:
        form = ExpenseForm(group)
    context = {
        'group': group,
        'form': form,
        'split_amount': split_amount,
    }
    return render(request, 'expense/expense.html', context)
