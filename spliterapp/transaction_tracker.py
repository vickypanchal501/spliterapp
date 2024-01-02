# transaction_tracker.py

from .models import RepaymentDetail

class TransactionTracker:
    def __init__(self):
        self.groups = {}
<<<<<<< HEAD

=======
        
>>>>>>> vicky
    def record_transaction(self, group, payer, payee, amount):
        if group not in self.groups:
            self.groups[group] = {}
        if payer not in self.groups[group]:
            self.groups[group][payer] = {}
        if payee not in self.groups[group][payer]:
            self.groups[group][payer][payee] = 0

<<<<<<< HEAD
        self.groups[group][payer][payee] += amount

        


    def split_and_record_transaction(self, payer, group_members, amount):
        split_amount = amount / len(group_members)
        for payee in group_members:
            if payer != payee:
                self.record_transaction(payer, payee, split_amount)

    def get_transactions(self, group, person):
        transactions_list = []
        dict1 = {}
        for payer, payees in self.groups.get(group, {}).items():
            for payee, amount in payees.items():
                if payer == person:
                    if payee not in dict1:
                        dict1[payee] = [amount]
                    else:
                        dict1[payee].append(amount)  
                    
                elif payee == person:
                    if payer not in dict1:
                        dict1[payer] = [-amount]
                    else:
                        dict1[payer].append(-amount)                       
                    
        print(dict1)
        for name , amount in dict1.items():
            if sum(amount) > 0 :
                transactions_list.append(f"{name}  {sum(amount)}")
            elif sum(amount) <0:    
                transactions_list.append(f"{name}  {sum(amount)}")
        return transactions_list
=======
        self.groups[group][payer][payee] += float(amount)
        print("group:-", self.groups)

    def split_and_record_transaction(self, group,payer, group_members, amount):
        if isinstance(group_members, dict):
            total_percentage = sum(group_members.values())
            print("sum(group_members.values())",sum(group_members.values()))
            for payee, percentage in group_members.items():
                if payer != payee:
                    print("payee:-",payee)
                    print("payer:-",payer)
                    split_amount = float(amount) * (percentage / float(total_percentage))
                    self.record_transaction(group, payer, payee, split_amount)
                    RepaymentDetail.record_repayment(payer, payee, group, split_amount)


    def get_transactions(self, group, person):
        dict1 = {}
        transactions_list = []

        # Query the database for repayment details
        repayments = RepaymentDetail.objects.filter(group=group)
        print(repayments)
        for repayment in repayments:
            payer = repayment.payer.username
            payee = repayment.payee.username
            amount = repayment.amount

            if payer == person:
                if payee not in dict1:
                    dict1[payee] = [amount]
                else:
                    dict1[payee].append(amount)
                # transactions_list.append(f"{payee} lent {payer} {amount}")
            elif payee == person:
                if payer not in dict1:
                    dict1[payer] = [-amount]     
                else:
                    dict1[payer].append(-amount)
        print(dict1)
        for user, amounts in dict1.items():
            total_amount = sum(amounts)
            if total_amount > 0:
                transactions_list.append({"user": user, "amount": total_amount, "color": "green" ,"person":person})
            else:
                transactions_list.append({"user": user, "amount": total_amount, "color": "red" , "person":person})

        return transactions_list
     
>>>>>>> vicky














<<<<<<< HEAD
=======
    # def split_and_record_transaction(self, payer, group_members, amount):
    #     split_amount = amount / len(group_members)
    #     for payee in group_members:
    #         if payer != payee:
    #             self.record_transaction(payer, payee, split_amount)

>>>>>>> vicky





    # def get_transactions(self, person, group):
    #     dict1 = {}
    #     transactions_list = []
    #     if group in self.transactions:
    #         for payer, payees in self.transactions[group].items():
    #             for payee, amount in payees.items():
    #                 if payer == person:
    #                     if payee not in dict1:
    #                         dict1[payee] = [amount]
    #                     else:
    #                         dict1[payee].append(amount)
    #                     transactions_list.append(f"{payee} lent {payer} {+amount}")
    #                     # Record repayment details in the database
    #                     RepaymentDetail.record_repayment(payee, payer, group, amount)
    #                 elif payee == person:
    #                     if payer not in dict1:
    #                         dict1[payer] = [-amount]
                            
    #                     else:
    #                         dict1[payer].append(-amount)
    #                     transactions_list.append(f"{payer} go back {-amount}")
    #                     # Record repayment details in the database
    #                     RepaymentDetail.record_repayment(payer, payee, group, -amount)

    #     return transactions_list
