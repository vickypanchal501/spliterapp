# Generated by Django 4.2.6 on 2023-11-21 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spliterapp', '0003_rename_split_amount_per_user_expense_amount_lent_by_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='paid_by_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
