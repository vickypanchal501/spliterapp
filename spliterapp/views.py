from django.shortcuts import render, redirect
from .models import Group, Expense
from account.models import CustomUser
from .forms import ExpenseForm

from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from .models import Group

from django.db.models import Sum
from collections import defaultdict



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
from decimal import Decimal


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
            pass

    group_expenses = Expense.objects.filter(group=group)

    # Calculate user balances in the group
    user_balances = {member: Decimal('0.0') for member in group.members.all()}

    # Update user_balances
    for member in group.members.all():
        expenses_lent = Expense.objects.filter(group=group, split_with=member)
        total_lent_amount = expenses_lent.aggregate(Sum('split_amount'))['split_amount__sum'] or Decimal('0.0')

        # Retrieve the paid amount from expenses
        expenses_paid = Expense.objects.filter(group=group, paid_by=member)
        total_paid_amount = expenses_paid.aggregate(Sum('amount_paid_by_user'))['amount_paid_by_user__sum'] or Decimal('0.0')

        # Calculate the balance for the user
        user_balances[member] = total_paid_amount - total_lent_amount

    # # Find the maximum get-back amount to adjust owes amounts
    # max_get_back = max(user_balances.values())

    # # Adjust user_balances for owes amounts
    # for member, balance in user_balances.items():
    #     if balance < 0:
    #         user_balances[member] += max_get_back

    context = {
        'group': group,
        'user_groups': user_groups,
        'user_id': user,
        'group_expenses': group_expenses[::-1],
        'user_balances': dict(user_balances),
    }

    return render(request, 'group/base.html', context)

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
            # split_with_users.append(request.user)
            expense.split_with.set(split_with_users)

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

            # Redirect to a different URL after successful form submission
            return redirect('group_detail', group_id=group.id)

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


def expense_detail(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)

    return render(request, 'expense/expense_details.html', {'expense': expense})


def user_detail(request, group_id, user_id):
    group = get_object_or_404(Group, id=group_id)
    user = get_object_or_404(CustomUser, id=user_id)

    # Calculate user balances in the group
    user_balances = {member: Decimal('0.0') for member in group.members.all()}

    # Update user_balances
    for member in group.members.all():
        expenses_lent = Expense.objects.filter(group=group, split_with=member)
        total_lent_amount = expenses_lent.aggregate(Sum('split_amount'))['split_amount__sum'] or Decimal('0.0')
        print("expenses_lent",expenses_lent)
        print("total_lent_amount",total_lent_amount)
        # Retrieve the paid amount from expenses
        expenses_paid = Expense.objects.filter(group=group, paid_by=member)
        total_paid_amount = expenses_paid.aggregate(Sum('amount_paid_by_user'))['amount_paid_by_user__sum'] or Decimal('0.0')
        print("expenses_paid",expenses_paid)
        print("total_paid_amount",total_paid_amount)
        # Calculate the balance for the user
        user_balances[member] = total_paid_amount - total_lent_amount
        print(user_balances[member])

    context = {
        'group': group,
        'user': user,
        'user_balances': user_balances,
    }

    return render(request, 'group/group_summary.html', context)
