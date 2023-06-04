# Generated by Django 4.0.3 on 2023-06-04 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
                ('phone', models.CharField(default='', max_length=50)),
                ('address', models.TextField()),
                ('zip_code', models.CharField(default='', max_length=10)),
            ],
        ),
    ]
