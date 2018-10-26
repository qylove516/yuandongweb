# Generated by Django 2.0.8 on 2018-10-14 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20181014_1112'),
    ]

    operations = [
        migrations.AddField(
            model_name='simpleimagepage',
            name='hans',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='中文'),
        ),
        migrations.AlterField(
            model_name='simpleimagepage',
            name='notes',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='英文'),
        ),
    ]