# Generated by Django 3.2.18 on 2023-09-06 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_commande_date_depot_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commande',
            name='Date_Depot_Model',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='commande',
            name='Date_Retrait_Model',
            field=models.DateTimeField(auto_now=True),
        ),
    ]