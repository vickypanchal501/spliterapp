from django.shortcuts import render, redirect
from .models import Group, Expense
from account.models import CustomUser
<<<<<<< HEAD
from .forms import ExpenseForm
=======
# from .forms import ExpenseForm 

>>>>>>> vikas

def create_group(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        creator = request.user
        group = Group.objects.create(name=group_name, creator=creator)
        group.members.add(creator)
        group.save()
        return redirect('group_detail', group_id=group.id)
<<<<<<< HEAD
    return render(request, 'group/base.html')

def group_detail(request, group_id):
    group = Group.objects.get(id=group_id)
    user = request.user
    user_groups = Group.objects.filter(members=user)

=======
    return render(request, 'group/main.html')

def group_detail(request, group_id):
    group = Group.objects.get(id=group_id)
    user = request.user  # Get the current user
    user_groups = Group.objects.filter(members=user)


>>>>>>> vikas
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
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> vikas
          
    return render(request, 'group/base.html', {'group': group, 'user_groups': user_groups, 'user_id': user })


def add_expense(request, group_id):
    group = Group.objects.get(id=group_id)
<<<<<<< HEAD
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
=======
    # import pdb; pdb.set_trace()
    if request.method == 'POST':
<<<<<<< HEAD
        form = ExpenseForm(group,request.POST)
=======
>>>>>>> parent of dfdcf37 (this is commit today add expense in admin07/11/2023)
=======
        form = ExpenseForm(request.POST)
>>>>>>> parent of 0701fcf (this is today commit enhance ui 08/11/20123)
        
    return render(request, 'group/main.html', {'group': group,'user_groups': user_groups, 'user_id': user })

def expense(request):
    return render(request, 'expense/expense.html')

# def add_expense(request, group_id):
#     group = Group.objects.get(id=group_id)
#     if request.method == 'POST':
#         form = ExpenseForm(request.POST)
#         if form.is_valid():
#             expense = form.save(commit=False)
#             expense.created_by = request.user
#             expense.group = group
#             expense.save()
#             return redirect('group_detail', group_id=group.id)
#     else:
#         form = ExpenseForm()
    return render(request, 'add_expense.html', {'form': form, 'group': group})


<<<<<<< HEAD
            return redirect('group_detail', group_id=group.id)
    else:
<<<<<<< HEAD
>>>>>>> vikas
        form = ExpenseForm(group)
    context = {
        'group': group,
        'form': form,
        'split_amount': split_amount,
    }
    return render(request, 'expense/expense.html', context)

def checkbox(request):
<<<<<<< HEAD
    return render(request, "expense/checkbox.html")
=======
    return render(request, "expense/checkbox.html")
=======


# def add_expense(request, group_id):
#     group = Group.objects.get(id=group_id)
#     if request.method == 'POST':
#         form = ExpenseForm(request.POST)
#         if form.is_valid():
#             expense = form.save(commit=False)
#             expense.created_by = request.user
#             expense.group = group
#             expense.save()

#             # Calculate the split amount
#             split_with_users = form.cleaned_data['split_with']
#             split_amount = form.cleaned_data['split_amount']

#             # Calculate the amount for each user
#             amount_per_user = split_amount / (len(split_with_users) + 1)
#             expense.split_amount = amount_per_user
#             expense.save()

#             # Add the creator to the split_with users
#             split_with_users = list(split_with_users)
#             split_with_users.append(request.user)
#             expense.split_with.set(split_with_users)

#             return redirect('group_detail', group_id=group.id)
#     else:
#         form = ExpenseForm()
#     return render(request, 'add_expense.html', {'form': form, 'group': group})
>>>>>>> parent of dfdcf37 (this is commit today add expense in admin07/11/2023)
=======
        form = ExpenseForm()

    return render(request, 'expense/expense.html', {'form': form, 'group': group})
>>>>>>> parent of 0701fcf (this is today commit enhance ui 08/11/20123)
>>>>>>> vikas
