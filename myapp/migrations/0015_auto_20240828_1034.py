# Generated by Django 3.2.12 on 2024-08-28 10:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_alter_appuntamento_stato'),
    ]

    operations = [
        migrations.AddField(
            model_name='pesata',
            name='idDottore',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pesata_dottore', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='pesata',
            name='idPaziente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pesata_paziente', to=settings.AUTH_USER_MODEL),
        ),
    ]
