# Generated by Django 3.2.12 on 2024-08-14 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_chat_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utente',
            name='foto_profilo',
            field=models.ImageField(default='images/default.jpg', upload_to='images/'),
        ),
    ]
