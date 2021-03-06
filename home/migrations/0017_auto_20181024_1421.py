# Generated by Django 2.0.8 on 2018-10-24 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_auto_20181020_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='productfirstpage',
            name='date',
            field=models.DateField(blank=True, null=True, verbose_name='发布日期'),
        ),
        migrations.AlterField(
            model_name='aboutitem',
            name='note',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='中文注释'),
        ),
        migrations.AlterField(
            model_name='aboutitem',
            name='note_en',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='英文注释'),
        ),
        migrations.AlterField(
            model_name='caseitem',
            name='note',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='中文注释'),
        ),
        migrations.AlterField(
            model_name='caseitem',
            name='note_en',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='英文注释'),
        ),
        migrations.AlterField(
            model_name='salebranditem',
            name='note',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='中文注释'),
        ),
        migrations.AlterField(
            model_name='salebranditem',
            name='note_en',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='英文注释'),
        ),
        migrations.AlterField(
            model_name='salehonoritem',
            name='note',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='中文注释'),
        ),
        migrations.AlterField(
            model_name='salehonoritem',
            name='note_en',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='英文注释'),
        ),
    ]
