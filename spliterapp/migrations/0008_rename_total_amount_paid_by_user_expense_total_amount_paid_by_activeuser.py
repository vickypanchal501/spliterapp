# Generated by Django 4.2.6 on 2023-11-28 07:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spliterapp', '0007_expense_total_amount_paid_by_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expense',
            old_name='total_amount_paid_by_user',
            new_name='total_amount_paid_by_activeuser',
        ),
    ]