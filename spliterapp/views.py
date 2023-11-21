from django.shortcuts import render, redirect
from .models import Group, Expense
from account.models import CustomUser
from .forms import ExpenseForm

from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from .models import Group

from django.db.models import Sum
def create_group(request):
    user = request.user
    user_groups = Group.objects.filter(members=user)
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        creator = request.user
        group = Group.objects.create(name=group_name, creator=creator)
        group.members.add(creator)
        group.save()
        return redirect('group_detail', group_id=group.id)
    return render(request, 'group/base.html' ,{'user_groups': user_groups,})

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

    if request.method == 'POST':
        form = ExpenseForm(group, request.POST)
        
        if form.is_valid():
            expense = form.save(commit=False)
            expense.created_by = request.user
            expense.group = group

            # Get split amount from the form
            split_amount = form.cleaned_data['split_amount']
            
            # Save the expense without calculating split amount for now
            expense.save()

            # Add the creator to the split_with users
            split_with_users = list(form.cleaned_data['split_with'])
            split_with_users.append(request.user)
            expense.split_with.set(split_with_users)

            # Calculate the amount for each user
            amount_per_user = split_amount / len(expense.split_with.all())
            expense.split_amount = amount_per_user
            expense.save()
            print(len(expense.split_with.all()))
             # Calculate amount paid by the user
            amount_paid_by_user = split_amount
            expense.amount_paid_by_user = amount_paid_by_user
            # Calculate amount lent (or owed) by the user
            # amount_lent_by_user = Expense.objects.filter(group=group, split_with=request.user).aggregate(Sum('split_amount'))['split_amount__sum'] or 0
            amount_lent_by_user =amount_per_user* (len(expense.split_with.all())-1)
            expense.amount_lent_by_user = amount_lent_by_user
            expense.save()

            return render(request, 'group/base.html', {
                'expenses': expense,
                
            })
    else:
        form = ExpenseForm(group)
    
    context = {
        'group': group,
        'form': form,
        'split_amount': split_amount,
    }
    return render(request, 'expense/expense.html', context)

def checkbox(request):
    return render(request, "expense/checkbox.html")



def delete_group(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    group.delete()
    return JsonResponse({'message': 'Group deleted successfully'})