# Generated by Django 4.0.3 on 2023-06-04 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.client'),
        ),
    ]
