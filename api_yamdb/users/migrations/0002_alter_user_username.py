# Generated by Django 3.2 on 2023-10-02 15:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(db_index=True, error_messages={'unique': 'Пользователь с таким именем уже существует.'}, max_length=150, unique=True, validators=[django.core.validators.RegexValidator(message='Неверное имя пользователя. ', regex='^[\\w]+[^@\\.\\+\\-]*$')]),
        ),
    ]
