from django.shortcuts import render, redirect
from .models import Group, Expense
from account.models import CustomUser
<<<<<<< HEAD
<<<<<<< HEAD
from .forms import ExpenseForm
=======
# from .forms import ExpenseForm 

>>>>>>> vikas
=======
from .forms import ExpenseForm
>>>>>>> vikcy

from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from .models import Group

from django.db.models import Sum
from collections import defaultdict
from decimal import Decimal



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
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> vikcy
    return render(request, 'group/base.html')

def group_detail(request, group_id):
    group = Group.objects.get(id=group_id)
    user = request.user
    user_groups = Group.objects.filter(members=user)

<<<<<<< HEAD
=======
    return render(request, 'group/main.html')

def group_detail(request, group_id):
    group = Group.objects.get(id=group_id)
    user = request.user  # Get the current user
    user_groups = Group.objects.filter(members=user)


>>>>>>> vikas
=======
>>>>>>> vikcy
=======

    return render(request, 'group/base.html', {'user_groups': user_groups})

def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    user_groups = Group.objects.filter(members=request.user)
    
>>>>>>> vicky
    if request.method == 'POST':
        invited_user_username = request.POST.get('invited_user')
        try:
            invited_user = CustomUser.objects.get(username=invited_user_username)
            if invited_user not in group.members.all():
                group.members.add(invited_user)
                group.save()
            return redirect('group_detail', group_id=group.id)
        except CustomUser.DoesNotExist:
            pass
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> vikas
          
    return render(request, 'group/base.html', {'group': group, 'user_groups': user_groups, 'user_id': user })
=======

    group_expenses = Expense.objects.filter(group=group)
    user_balances = calculate_user_balances(group)
    settle_up_details = calculate_settle_up_details(user_balances)

    context = {
        'group': group,
        'user_groups': user_groups,
        'user_id': request.user,
        'group_expenses': group_expenses[::-1],
        'user_balances': dict(user_balances),
        'settle_up_details': settle_up_details,
    }

    return render(request, 'group/base.html', context)
>>>>>>> vicky


def add_expense(request, group_id):
    group = Group.objects.get(id=group_id)
<<<<<<< HEAD
<<<<<<< HEAD
    split_amount = 0 
    # import pdb; pdb.set_trace()
    if request.method == 'POST':
        form = ExpenseForm(group,request.POST)
        
=======
          
    return render(request, 'group/base.html', {'group': group, 'user_groups': user_groups, 'user_id': user })

  # Import your UserExpense model

def add_expense(request, group_id):
    group = Group.objects.get(id=group_id)
    split_amount = 0

    if request.method == 'POST':
        form = ExpenseForm(group, request.POST)

>>>>>>> vikcy
=======
    split_amount = 0

    if request.method == 'POST':
        form = ExpenseForm(group, request.POST)

>>>>>>> vicky
        if form.is_valid():
            expense = form.save(commit=False)
            expense.created_by = request.user
            expense.group = group

            # Get split amount from the form
            split_amount = form.cleaned_data['split_amount']

<<<<<<< HEAD
            # Calculate the amount for each user
<<<<<<< HEAD
            amount_per_user = split_amount / (len(split_with_users) + 1)
            expense.split_amount = amount_per_user
=======
            # Save the expense without calculating split amount for now
>>>>>>> vicky
            expense.save()
=======
            
            # Save the split amount for each selected user
            # for user in split_with_users:
            #     UserExpense.objects.create(expense=expense, user=user, split_amount=amount_per_user)
>>>>>>> vikcy

            # Add the creator to the split_with users
            split_with_users = list(form.cleaned_data['split_with'])
            # split_with_users.append(request.user)
            expense.split_with.set(split_with_users)
<<<<<<< HEAD

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
=======
            split_amount_per_user = split_amount / (len(split_with_users) + 1)

            # Calculate the amount for each user
            amount_per_user = split_amount / len(expense.split_with.all())
            expense.split_amount = amount_per_user
            expense.save()
            

            # Set lent amount based on whether the current user is a member of the group
            is_member = request.user in expense.split_with.all()
            
            # Calculate amount lent (or owed) by the user
            amount_lent_by_user = amount_per_user * (len(expense.split_with.all()) - 1)
            expense.amount_lent_by_user = amount_lent_by_user  if is_member else split_amount
            # Calculate amount paid by the user
            expense.amount_paid_by_user = split_amount if is_member else split_amount

            expense.save()
            if expense.created_by == expense.paid_by:
                expense.total_amount_paid_by_activeuser  = split_amount
            else:
                expense.total_amount_paid_by_activeuser  = 0 

            expense.save()

            payer = expense.paid_by.username
            for payee in expense.split_with.all():
                if payer != payee.username: 
                    transaction_tracker.record_transaction( group,payer, payee.username, amount_per_user, )
                    RepaymentDetail.record_repayment(payer, payee.username, group, amount_per_user)


            # Redirect to a different URL after successful form submission
            return redirect('group_detail', group_id=group.id)

    else:
        form = ExpenseForm(group)

<<<<<<< HEAD
>>>>>>> vikcy
=======
>>>>>>> vicky
    context = {
        'group': group,
        'form': form,
        'split_amount': split_amount,
    }
    return render(request, 'expense/expense.html', context)

def checkbox(request):
<<<<<<< HEAD
<<<<<<< HEAD
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
=======
    return render(request, "expense/checkbox.html")
>>>>>>> vikcy
=======
    return render(request, "expense/checkbox.html")



def delete_group(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    group.delete()
    return JsonResponse({'message': 'Group deleted successfully'})


def expense_detail(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    settlements = expense.get_settlements()
    

    return render(request, 'expense/expense_details.html', {'expense': expense, 'settlements': settlements,})


# def calculate_user_balances(group):
#     user_balances = {member: Decimal('0.0') for member in group.members.all()}
    
#     for member in group.members.all():
#         expenses_lent = Expense.objects.filter(group=group, split_with=member)
#         total_lent_amount = expenses_lent.aggregate(Sum('split_amount'))['split_amount__sum'] or Decimal('0.0')

#         expenses_paid = Expense.objects.filter(group=group, paid_by=member)
#         total_paid_amount = expenses_paid.aggregate(Sum('amount_paid_by_user'))['amount_paid_by_user__sum'] or Decimal('0.0')

#         user_balances[member] = total_paid_amount - total_lent_amount
#         print(user_balances[member])
        
#     return user_balances


def calculate_user_balances(group):
    user_balances = {member: Decimal('0.0') for member in group.members.all()}
    
    for expense in Expense.objects.filter(group=group):
        # Calculate amount lent by the user
        amount_lent_by_user = expense.amount_lent_by_user or Decimal('0.0')
        user_balances[expense.paid_by] += amount_lent_by_user

        # Calculate amount paid by the user
        amount_paid_by_user = expense.amount_paid_by_user or Decimal('0.0')
        user_balances[expense.paid_by] -= amount_paid_by_user

        # Calculate split amounts for each user involved
        for user in expense.split_with.all():
            if user != expense.paid_by:
                user_balances[user] += expense.split_amount

    return user_balances

def calculate_settle_up_details(user_balances):
    owes = defaultdict(Decimal)
    gets_back = defaultdict(Decimal)

    for creditor, amount in user_balances.items():
        if amount < 0:
            for debtor, debt_amount in user_balances.items():
                if debt_amount > 0:
                    settles = min(abs(amount), debt_amount)
                    owes[debtor] += settles
                    gets_back[creditor] += settles
                    amount += settles
                    debt_amount -= settles

    return {'owes': dict(owes), 'gets_back': dict(gets_back)}
def suggested_repayments(request, group_id, user_id):
    group = get_object_or_404(Group, id=group_id)
    user = get_object_or_404(CustomUser, id=user_id)
    user_balances = calculate_user_balances(group)
    settle_up_details = calculate_settle_up_details(user_balances)

    suggested_repayments = {
        'owes': {other_user: amount for other_user, amount in settle_up_details['owes'].items() if other_user != user},
        'gets_back': {other_user: amount for other_user, amount in settle_up_details['gets_back'].items() if other_user != user},
    }

    context = {
        'group': group,
        'user': user,
        'suggested_repayments': suggested_repayments,
    }

    return render(request, 'group/suggested_repayments.html', context)

def detailed_repayments(request, group_id, user_id):
    group = get_object_or_404(Group, id=group_id)
    user = get_object_or_404(CustomUser, id=user_id)
    user_balances = calculate_user_balances(group)
    settle_up_details = calculate_settle_up_details(user_balances)

    detailed_repayments = []

    for other_user, amount in settle_up_details['owes'].items():
        detailed_repayments.append({
            'from_user': other_user,
            'to_user': user,
            'amount': amount,
        })

    for other_user, amount in settle_up_details['gets_back'].items():
        detailed_repayments.append({
            'from_user': user,
            'to_user': other_user,
            'amount': amount,
        })

    context = {
        'group': group,
        'user': user,
        'detailed_repayments': detailed_repayments,
    }

    return render(request, 'group/detailed_repayments.html', context)
>>>>>>> vicky
