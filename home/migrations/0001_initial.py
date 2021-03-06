# Generated by Django 2.0.8 on 2018-10-09 16:33

from django.db import migrations, models
import django.db.models.deletion
import home.models
import modelcluster.fields
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailimages', '0021_image_file_hash'),
        ('wagtailcore', '0040_page_draft_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddonScriptsSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('head', models.TextField(blank=True, default='', help_text='添加到head的脚本', verbose_name='head')),
                ('body', models.TextField(blank=True, default='', help_text='添加到body的脚本', verbose_name='body')),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.Site')),
            ],
            options={
                'verbose_name': '附加功能脚本',
            },
        ),
        migrations.CreateModel(
            name='FormField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('label', models.CharField(help_text='The label of the form field', max_length=255, verbose_name='label')),
                ('field_type', models.CharField(choices=[('singleline', 'Single line text'), ('multiline', 'Multi-line text'), ('email', 'Email'), ('number', 'Number'), ('url', 'URL'), ('checkbox', 'Checkbox'), ('checkboxes', 'Checkboxes'), ('dropdown', 'Drop down'), ('multiselect', 'Multiple select'), ('radio', 'Radio buttons'), ('date', 'Date'), ('datetime', 'Date/time'), ('hidden', 'Hidden field')], max_length=16, verbose_name='field type')),
                ('required', models.BooleanField(default=True, verbose_name='required')),
                ('choices', models.TextField(blank=True, help_text='Comma separated list of choices. Only applicable in checkboxes, radio and dropdown.', verbose_name='choices')),
                ('default_value', models.CharField(blank=True, help_text='Default value. Comma separated values supported for checkboxes.', max_length=255, verbose_name='default value')),
                ('help_text', models.CharField(blank=True, max_length=255, verbose_name='help text')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FormPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('to_address', models.CharField(blank=True, help_text='Optional - form submissions will be emailed to these addresses. Separate multiple addresses by comma.', max_length=255, verbose_name='to address')),
                ('from_address', models.CharField(blank=True, max_length=255, verbose_name='from address')),
                ('subject', models.CharField(blank=True, max_length=255, verbose_name='subject')),
                ('name', models.CharField(max_length=64, null=True, verbose_name='联系人')),
                ('address', models.CharField(max_length=256, null=True, verbose_name='地址')),
                ('tel', models.CharField(max_length=32, null=True, verbose_name='电话')),
                ('fax', models.CharField(max_length=32, null=True, verbose_name='传真')),
                ('QQ', models.IntegerField(null=True, verbose_name='QQ')),
                ('email', models.EmailField(max_length=64, null=True, verbose_name='邮箱')),
                ('thank_you_text', models.TextField(blank=True)),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
                ('qr_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image', verbose_name='微信二维码')),
            ],
            options={
                'verbose_name': '在线留言',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'verbose_name': '主页',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='HomePageCarouselItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('embed_url', models.URLField(blank=True, verbose_name='Embed URL')),
                ('caption', models.TextField(blank=True, max_length=255)),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='carousel_items', to='home.HomePage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NavMenuItem',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('embellish_title', models.CharField(blank=True, max_length=32, null=True, verbose_name='修饰标题')),
                ('show_in_sub_menus', models.BooleanField(default=False, verbose_name='二级页面菜单显示')),
            ],
            options={
                'verbose_name': '主导航栏菜单项',
                'verbose_name_plural': '主导航栏菜单项',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='SiteInfoSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=256, verbose_name='专卖店名称')),
                ('left_content', models.CharField(max_length=64, verbose_name='左栏')),
                ('center_content', models.CharField(max_length=64, verbose_name='中栏')),
                ('right_content', models.CharField(max_length=64, verbose_name='右栏')),
                ('logo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image', verbose_name='商标')),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.Site')),
                ('tel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image', verbose_name='联系方式')),
            ],
            options={
                'verbose_name': '网站信息',
            },
        ),
        migrations.CreateModel(
            name='AboutFirstPage',
            fields=[
                ('navmenuitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.NavMenuItem')),
            ],
            options={
                'verbose_name': '关于我们一级页面',
                'verbose_name_plural': '关于我们一级页面',
            },
            bases=('home.navmenuitem',),
        ),
        migrations.CreateModel(
            name='CaseFirstPage',
            fields=[
                ('navmenuitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.NavMenuItem')),
            ],
            options={
                'verbose_name': '案例一级页面',
                'verbose_name_plural': '案例一级页面',
            },
            bases=('home.navmenuitem',),
        ),
        migrations.CreateModel(
            name='CompanyHonorPage',
            fields=[
                ('navmenuitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.NavMenuItem')),
            ],
            options={
                'verbose_name': '公司荣誉墙',
            },
            bases=('home.navmenuitem',),
        ),
        migrations.CreateModel(
            name='NewsFirstPage',
            fields=[
                ('navmenuitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.NavMenuItem')),
            ],
            options={
                'verbose_name': '新闻一级页面',
                'verbose_name_plural': '新闻一级页面',
            },
            bases=('home.navmenuitem',),
        ),
        migrations.CreateModel(
            name='ProductFirstPage',
            fields=[
                ('navmenuitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.NavMenuItem')),
            ],
            options={
                'verbose_name': '产品一级页面',
                'verbose_name_plural': '产品一级页面',
            },
            bases=('home.navmenuitem',),
        ),
        migrations.CreateModel(
            name='SaleBrandPage',
            fields=[
                ('navmenuitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.NavMenuItem')),
            ],
            options={
                'verbose_name': '专卖店形象',
            },
            bases=('home.navmenuitem',),
        ),
        migrations.CreateModel(
            name='SaleHonorPage',
            fields=[
                ('navmenuitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.NavMenuItem')),
            ],
            options={
                'verbose_name': '专卖店荣誉',
            },
            bases=('home.navmenuitem',),
        ),
        migrations.CreateModel(
            name='SimpleImagePage',
            fields=[
                ('navmenuitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.NavMenuItem')),
                ('date', models.DateField(verbose_name='发布日期')),
                ('notes', models.CharField(blank=True, max_length=64, null=True, verbose_name='备注')),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image', verbose_name='图片')),
            ],
            options={
                'verbose_name': '图片通用二级',
            },
            bases=('home.navmenuitem',),
        ),
        migrations.CreateModel(
            name='SubArticlePage',
            fields=[
                ('navmenuitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.NavMenuItem')),
                ('date', models.DateField(verbose_name='发布日期')),
                ('summary', models.TextField(blank=True, max_length=255, verbose_name='摘要')),
                ('body', wagtail.core.fields.StreamField([('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow', label='段落')), ('aligned_image', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('caption', wagtail.core.blocks.TextBlock(required=True)), ('alignment', home.models.ImageFormatChoiceBlock())], icon='image', label='图片'))])),
                ('top', models.BooleanField(default=False, verbose_name='置顶')),
            ],
            options={
                'verbose_name': '通用二级文章页面',
                'verbose_name_plural': '通用二级文章页面',
            },
            bases=('home.navmenuitem',),
        ),
        migrations.AddField(
            model_name='navmenuitem',
            name='cover_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image', verbose_name='封面图片'),
        ),
        migrations.AddField(
            model_name='navmenuitem',
            name='link_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page', verbose_name='跳转链接'),
        ),
        migrations.AddField(
            model_name='navmenuitem',
            name='sub_nav_parent_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page', verbose_name='子菜单上级页面'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='about_parent',
            field=models.ForeignKey(blank=True, help_text='介绍公司及专卖店', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page', verbose_name='关于我们'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='case_parent',
            field=models.ForeignKey(blank=True, help_text='展示最近的工程案例图片', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page', verbose_name='工程案例'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='contract_us_parent',
            field=models.ForeignKey(blank=True, help_text='专卖店的联系方式', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page', verbose_name='联系我们'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='news_parent',
            field=models.ForeignKey(blank=True, help_text='专卖店最新信息动态', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page', verbose_name='专卖店新闻'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='product_parent',
            field=models.ForeignKey(blank=True, help_text='产品中心信息动态', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page', verbose_name='产品中心'),
        ),
        migrations.AddField(
            model_name='formfield',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='form_fields', to='home.FormPage'),
        ),
    ]
