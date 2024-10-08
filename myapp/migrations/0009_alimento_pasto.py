# Generated by Django 5.0.7 on 2024-08-05 13:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_cura_statorichiesta'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alimento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=30)),
                ('proteine', models.FloatField(blank=True, default=0)),
                ('grassi', models.FloatField(blank=True, default=0)),
                ('carboidrati', models.FloatField(blank=True, default=0)),
                ('calorie', models.FloatField(blank=True, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Pasto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(blank=True, max_length=1)),
                ('giorno', models.CharField(blank=True, max_length=9)),
                ('qta', models.FloatField(blank=True, default=None)),
                ('idDieta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.dieta')),
                ('idalimento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.alimento')),
            ],
        ),
    ]
