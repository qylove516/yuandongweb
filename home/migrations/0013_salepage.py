# Generated by Django 2.0.8 on 2018-10-16 22:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_auto_20181016_2218'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalePage',
            fields=[
                ('subarticlepage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.SubArticlePage')),
            ],
            options={
                'verbose_name': '简介',
            },
            bases=('home.subarticlepage',),
        ),
    ]
