# Generated by Django 4.2.6 on 2023-11-06 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spliterapp', '0002_expense'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='amount',
            field=models.IntegerField(default=0),
        ),
    ]
