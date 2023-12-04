# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Group, Expense ,RepaymentDetail
from account.models import CustomUser
from .forms import ExpenseForm
from collections import defaultdict
from decimal import Decimal
from .transaction_tracker import TransactionTracker

transaction_tracker = TransactionTracker()

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

    return render(request, 'group/base.html', {'user_groups': user_groups})

def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    user_groups = Group.objects.filter(members=request.user)

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
    user_balances = group.members.all()
    # user_balances = calculate_user_balances(group)



    context = {
        'group': group,
        'user_groups': user_groups,
        'user_id': request.user,
        'group_expenses': group_expenses[::-1],
        'user_balances': user_balances,
        # 'user_owe_details': user_owe_details,
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
            amount = form.cleaned_data['split_amount']
            expense.amount = amount  # Corrected this line
            # Save the expense without calculating split amount for now
            expense.save()

            # Add the creator to the split_with users
            split_with_users = list(form.cleaned_data['split_with'])
            # split_with_users.remove(request.user)
            expense.split_with.set(split_with_users)

            # Calculate the amount for each user
            amount_per_user = amount / len(expense.split_with.all())
            expense.split_amount = amount_per_user
            expense.save()

            # Set lent amount based on whether the current user is a member of the group
            is_member = request.user in expense.split_with.all()

            # Calculate the total number of members in the expense group
            total_members = len(expense.split_with.all())

            # Calculate the amount per user
            amount_per_user = expense.amount / total_members

            # Calculate amount lent (or owed) by the user
            amount_lent_by_user = amount_per_user * (total_members - 1)
            expense.amount_lent_by_user = amount_per_user if is_member else 0  # Adjusted this line

            # Calculate amount paid by the user
            expense.amount_paid_by_user = amount if is_member else 0
            expense.save()

            if expense.created_by == expense.paid_by:
                expense.total_amount_paid_by_activeuser = amount
            else:
                expense.total_amount_paid_by_activeuser = 0

            expense.save()
            payer = expense.paid_by.username
            for payee in expense.split_with.all():
                if payer != payee.username: 
                    transaction_tracker.record_transaction(group,payer, payee.username, amount_per_user, )
                    RepaymentDetail.record_repayment(payer, payee, group, amount_per_user)


            print("expense.total_amount_paid_by_activeuser:", expense.total_amount_paid_by_activeuser)
            print("expense.amount_paid_by_user:", expense.amount_paid_by_user)
            print("expense.amount_lent_by_user:", expense.amount_lent_by_user)
            print("amount_per_user:", amount_per_user)
            print("split_amount:", expense.split_amount)
            print("expense.amount:", expense.amount)
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


def detailed_repayments(request, group_id, user_id):
    group = get_object_or_404(Group, id=group_id)
    user = get_object_or_404(CustomUser, id=user_id)
    # expense = get_object_or_404(Expense, id=expense_id)
    transactions = transaction_tracker.get_transactions(group,user.username, )

    context = {
        'user': user,
        'group': group,
        'transactions': transactions,
    }
    return render(request, 'group/detailed_repayments.html', context)