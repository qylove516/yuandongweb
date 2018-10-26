# Generated by Django 2.0.8 on 2018-10-09 20:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0040_page_draft_title'),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepage',
            name='about_parent',
        ),
        migrations.AddField(
            model_name='homepage',
            name='company_honor_parent',
            field=models.ForeignKey(blank=True, help_text='公司荣誉', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page', verbose_name='公司荣誉'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='sale_brand_parent',
            field=models.ForeignKey(blank=True, help_text='专卖店形象', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page', verbose_name='专卖店形象'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='sale_honor_parent',
            field=models.ForeignKey(blank=True, help_text='专卖店荣誉', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page', verbose_name='专卖店荣誉'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='sale_parent',
            field=models.ForeignKey(blank=True, help_text='专卖店介绍', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page', verbose_name='专卖店介绍'),
        ),
    ]
