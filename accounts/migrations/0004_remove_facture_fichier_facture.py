# Generated by Django 4.2.4 on 2023-08-29 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_facture_fichier_facture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facture',
            name='fichier_facture',
        ),
    ]
