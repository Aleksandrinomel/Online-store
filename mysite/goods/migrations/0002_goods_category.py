# Generated by Django 2.1.2 on 2018-10-13 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='category',
            field=models.TextField(null=True),
        ),
    ]
