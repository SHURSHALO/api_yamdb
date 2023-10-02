# Generated by Django 3.2 on 2023-10-02 17:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='confirmation_code',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Код потдверждения'),
        ),
    ]
