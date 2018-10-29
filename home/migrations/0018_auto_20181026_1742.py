# Generated by Django 2.0.8 on 2018-10-26 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_auto_20181024_1421'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebSite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': '相关网站',
            },
        ),
        migrations.AlterField(
            model_name='siteinfosetting',
            name='name',
            field=models.CharField(blank=True, max_length=256, verbose_name='专卖店总站'),
        ),
        migrations.AlterField(
            model_name='subarticlepage',
            name='author',
            field=models.CharField(blank=True, max_length=32, verbose_name='作者/来源'),
        ),
    ]
