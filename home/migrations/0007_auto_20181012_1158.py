# Generated by Django 2.0.8 on 2018-10-12 11:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_productkindpage_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productkindpage',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='时间'),
        ),
    ]
