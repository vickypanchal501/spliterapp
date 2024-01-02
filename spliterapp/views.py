# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Group, Expense ,RepaymentDetail
from account.models import CustomUser
from .forms import ExpenseForm
from collections import defaultdict
from decimal import Decimal
from .transaction_tracker import TransactionTracker
from django.db.models import Sum
from decimal import Decimal
from django.contrib import messages
transaction_tracker = TransactionTracker()



def calculate_user_balances(group):
    user_balances = {}

    for member in group.members.all():
        aggregated_amount = member.expenses_involved.filter(group=group).aggregate(Sum('amount'))['amount__sum']
        user_balances[member] = -aggregated_amount if aggregated_amount is not None else Decimal('0.0')

    return user_balances



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
        if invited_user_username:
            try:
                invited_user = CustomUser.objects.get(username=invited_user_username)
                if invited_user not in group.members.all():
                    group.members.add(invited_user)
                    messages.success(request, f"{invited_user.username} added to the group.")
                else:
                    messages.error(request, f"User with username {invited_user_username} not found.")

            except CustomUser.DoesNotExist:
                # invited_user_username =  None
                messages.error(request, f"User with username {invited_user_username} not found.")
 
        group.save()

    group_expenses = Expense.objects.filter(group=group)


    group_members = group.members.all()
    user = request.user
    if user not in group_members:
        return redirect('Main')
    # user_balances = group.members.all()
    # user_balances = calculate_user_balances(group)
    # user_balances = {member: Decimal('0.0') for member in group.members.all()}
    user_balances = calculate_user_balances(group)

    for user in group_members:
        dict1 = {}
        # Query the database for repayment details
        repayments = RepaymentDetail.objects.filter(group=group)
  
        for repayment in repayments:
            payer = repayment.payer
            payee = repayment.payee
            amount = repayment.amount

            if payer == user:
                if payee not in dict1:
                    dict1[payee] = amount
                else:
                    dict1[payee] += amount
            elif payee == user:
                if payer not in dict1:
                    dict1[payer] = -amount     
                else:
                    dict1[payer] += - amount 
        # print(dict1)
        for users, values in dict1.items():
            user_balances[users] += values
    context = {
        'group': group,
        'user_groups': user_groups,
        'user_id': request.user,
        'group_expenses': group_expenses[::-1],
        'user_balances': dict(user_balances),
        # 'user_owe_details': user_owe_details,
    }

    return render(request, 'group/base.html', context)
def add_expense(request, group_id):
    group = Group.objects.get(id=group_id)
    group_members = group.members.all()
    user = request.user
    if user not in group_members:
        return redirect('Main')

    if request.method == 'POST':
        form = ExpenseForm(group, request.POST)

        if form.is_valid():
            expense = form.save(commit=False)
            expense.created_by = request.user
            expense.group = group
            amount = form.cleaned_data['split_amount']
            expense.amount = amount  # Corrected this line
            expense.save()
            split_with_users = list(form.cleaned_data['split_with'])
            expense.split_with.set(split_with_users)
            amount_per_user = amount / len(expense.split_with.all())
            expense.split_amount = amount_per_user
            expense.save()
            is_member = request.user in expense.split_with.all()
            total_members = len(expense.split_with.all())
            amount_per_user = expense.amount / total_members
            split_type = request.POST.get('split_type')

            if split_type == 'percentage':
                group_members = {user.username: float(request.POST.get(f"contributions[{user.username}]")) for user in group.members.all()}
                total_percentage = sum(group_members.values())
                amount_percentage_total = 0
                not_active_user_paid = 0
                payer = expense.paid_by.username

                for payee, percentage in group_members.items():
                    expense.percentages[payee] = float(float(expense.amount) * (percentage / float(total_percentage)))
                    # print(percentage[payee]) 
                  
                    # print("payee", type(payee))
                    # for key , value in expense.percentages.items():
                    #     print("keys:- ", key , "value:- ", value)
                    if payer != payee:
                        if payee == request.user.username:
                            split_amount = float(expense.amount) * (percentage / float(total_percentage))
                            transaction_tracker.record_transaction(group, payer, payee, split_amount)
                            RepaymentDetail.record_repayment(payer, payee, group, split_amount)
                            not_active_user_paid += split_amount
                        else:
                            split_amount = float(expense.amount) * (percentage / float(total_percentage))
                            transaction_tracker.record_transaction(group, payer, payee, split_amount)
                            RepaymentDetail.record_repayment(payer, payee, group, split_amount)
                            amount_percentage_total += split_amount    

                if request.user == expense.paid_by:
                    expense.amount_paid_by_user = amount if is_member else 0
                    expense.amount_lent_by_user = amount_percentage_total  if is_member else 0
                else:
                    expense.amount_paid_by_user = amount if is_member else 0
                    expense.amount_lent_by_user = not_active_user_paid  if is_member else 0
                    expense.save()
            else:
                payer = expense.paid_by.username
                for payee in expense.split_with.all():
                    expense.percentages[payee.username] = float(amount_per_user)
                    if payer != payee.username: 
                        transaction_tracker.record_transaction(group,payer, payee.username, amount_per_user, )
                        RepaymentDetail.record_repayment(payer, payee.username, group, amount_per_user)
                if request.user == expense.paid_by:                                # Update amount_paid_by_user and amount_lent_by_user
                    expense.amount_paid_by_user = amount if is_member else 0
                    expense.amount_lent_by_user = amount - amount_per_user if is_member else 0
                else:
                    expense.amount_paid_by_user = amount if is_member else 0
                    expense.amount_lent_by_user =  amount_per_user if is_member else 0


            if expense.created_by == expense.paid_by:
                expense.total_amount_paid_by_activeuser = amount
            else:
                expense.total_amount_paid_by_activeuser = 0
            expense.save()
            

            return redirect('group_detail', group_id=group.id)


"dkasd"
    else:
        form = ExpenseForm(group)

    context = {
        'group': group,
        'form': form,
        # 'split_amount': split_amount,
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
    group_members = group.members.all()
    users = request.user
    if users not in group_members:
        return redirect('Main')
    print("group",group)
    transactions = transaction_tracker.get_transactions(group,user.username, )
    for transaction in transactions:
        transaction['abs_amount'] = abs(transaction['amount'])
    context = {
        'user': user,
        'group': group,
        'transactions': transactions,
    }
    return render(request, 'group/detailed_repayments.html', context)