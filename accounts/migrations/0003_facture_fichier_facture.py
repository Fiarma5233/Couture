# Generated by Django 4.2.4 on 2023-08-29 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_facture_telephone'),
    ]

    operations = [
        migrations.AddField(
            model_name='facture',
            name='fichier_facture',
            field=models.FileField(default=1, upload_to='factures/'),
            preserve_default=False,
        ),
    ]
