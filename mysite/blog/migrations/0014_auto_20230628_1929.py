# Generated by Django 3.1.3 on 2023-06-28 18:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_commande'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='client',
        ),
        migrations.RemoveField(
            model_name='commande',
            name='provider',
        ),
    ]
