from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models
from django import forms
import django.utils.timezone as timezone

from modelcluster.fields import ParentalKey
from slugify import slugify
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel, \
    FieldRowPanel
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.core.blocks import StreamBlock, StructBlock, TextBlock, RichTextBlock, FieldBlock, CharBlock
from wagtail.core.fields import StreamField
from wagtail.snippets.models import register_snippet

from wagtail.core.models import Page, Orderable
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField


class CarouselItem(models.Model):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    embed_url = models.URLField("Embed URL", blank=True)
    caption = models.TextField(max_length=255, blank=True)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('embed_url'),
        FieldPanel('caption'),
    ]

    class Meta:
        abstract = True


# 主导航栏菜单项
class NavMenuItem(Page):
    embellish_title = models.CharField("修饰标题", max_length=32, blank=True, null=True)
    cover_image = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name="封面图片",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    link_page = models.ForeignKey(
        "wagtailcore.Page",
        verbose_name="跳转链接",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    sub_nav_parent_page = models.ForeignKey(
        "wagtailcore.Page",
        verbose_name="子菜单上级页面",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    show_in_sub_menus = models.BooleanField("二级页面菜单显示", default=False)

    @property
    def section_page(self):
        """获取所属的一级导航页面"""
        ancestors = self.get_ancestors(True)
        if len(ancestors) > 2:
            return ancestors[2].specific
        return ancestors[len(ancestors) - 1]

    @property
    def sub_menu_pages(self):
        """获取需要显示在二级导航中的页面"""
        return NavMenuItem.objects.child_of(self).filter(
            live=True,
            show_in_sub_menus=True,
        )

    @property
    def parent_specific(self):
        parent = self.get_parent().specific
        try:
            if parent.sub_nav_parent_page:
                parent = parent.sub_nav_parent_page.specific
        except AttributeError:
            pass
        return parent

    def get_context(self, request, *args, **kwargs):
        context = super(NavMenuItem, self).get_context(request)
        context["parent_title"] = self.parent_specific
        context["section_page"] = self.section_page
        if isinstance(self.parent_specific, NavMenuItem):
            context["parent_embellish_title"] = self.parent_specific.embellish_title
        context["menu_pages"] = NavMenuItem.objects.child_of(self.section_page).filter(
            live=True,
            show_in_menus=True,
        )
        return context

    def save(self, *args, **kwargs):
        self.slug = slugify(self.slug)
        super(NavMenuItem, self).save(*args, **kwargs)

    promote_panels = Page.promote_panels + [
        MultiFieldPanel(
            [
                FieldPanel('embellish_title'),
                ImageChooserPanel("cover_image"),
                PageChooserPanel("link_page"),
                PageChooserPanel("sub_nav_parent_page"),
                FieldPanel("show_in_sub_menus"),
            ],
            heading="菜单属性"
        )
    ]

    class Meta:
        verbose_name = "主导航栏菜单项"
        verbose_name_plural = "主导航栏菜单项"


class AboutCarouse(models.Model):
    """关于我们图片与说明"""
    image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="图片",
        related_name="+",
    )
    note = models.CharField("中文注释", max_length=64, blank=True, null=True)
    note_en = models.CharField("英文注释", max_length=64, blank=True, null=True)
    panels = [
        ImageChooserPanel("image"),
        FieldPanel("note"),
        FieldPanel("note_en"),
    ]

    class Meta:
        abstract = True


class ImageFormatChoiceBlock(FieldBlock):
    """图片格式选择区块"""
    field = forms.ChoiceField(choices=(
        ('default', '默认'), ('left', '靠左'), ('right', '靠右'), ('mid', '居中'), ('mid-avatar', '居中头像'), ('full', '页面宽度'),
    ))


class ImageBlock(StructBlock):
    """
    图片区块
    """
    image = ImageChooserBlock()
    caption = TextBlock(required=True)
    alignment = ImageFormatChoiceBlock()


# 文章项目基础，为文章页面 body 选项
class AticleStreamBlock(StreamBlock):
    h2 = CharBlock(icon="title", label='2号标题', classname="title")
    h3 = CharBlock(icon="title", label='3号标题', classname="title")
    h4 = CharBlock(icon="title", label='4号标题', classname="title")
    paragraph = RichTextBlock(icon="pilcrow", label="段落")
    aligned_image = ImageBlock(icon="image", label="图片")


# 通用二级文章页面 （新闻、产品、关于我们）
class SubArticlePage(NavMenuItem):
    author = models.CharField("作者/来源", max_length=32, blank=True)
    date = models.DateField("发布日期")
    summary = models.TextField("摘要", max_length=255, blank=True)
    body = StreamField(AticleStreamBlock())
    top = models.BooleanField("置顶", default=False)
    image = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name="缩略图",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="请按要求上传规定尺寸的图片，如尺寸不一样，请务必保持比例一致"
    )
    subpage_types = []

    @property
    def author_name(self):
        if self.author:
            author = self.author
            return author
        else:
            author = "{last_name}{first_name}".format(
                last_name=self.owner.last_name,
                first_name=self.owner.first_name
            )
            return author

    content_panels = NavMenuItem.content_panels + [
        FieldPanel('top'),
        FieldPanel('author'),
        FieldPanel('date'),
        ImageChooserPanel("image"),
        FieldPanel('summary'),
        StreamFieldPanel('body'),
    ]

    class Meta:
        verbose_name = "通用二级文章页面"
        verbose_name_plural = "通用二级文章页面"


# 关于我们一级页面
class AboutFirstPage(NavMenuItem):
    subpage_types = [
        "home.SalePage",
        "home.SaleBrandPage",
        "home.CompanyHonorPage",
        "home.SaleHonorPage",
    ]

    @property
    def banner_image(self):
        return self.cover_image

    @property
    def about_us(self):
        # 获取本页面子页面中已发布的页面
        about_us = SalePage.objects.live().descendant_of(self)[0]
        return about_us

    @property
    def company_honor(self):
        try:
            company_honor = CompanyHonorPage.objects.live().descendant_of(self)[0]
            return company_honor
        except:
            pass

    @property
    def sale_honor(self):
        try:
            sale_honor = SaleHonorPage.objects.live().descendant_of(self)[0]
            return sale_honor
        except:
            pass

    @property
    def sale_brand(self):
        try:
            sale_brand = SaleBrandPage.objects.live().descendant_of(self)[0]
            return sale_brand
        except:
            pass

    def get_context(self, request, *args, **kwargs):
        context = super(AboutFirstPage, self).get_context(request)
        context["company_content"] = self.company_honor.specific.about_company_item.all()
        context["sale_honor_content"] = self.sale_honor.specific.sale_honor_item.all()
        context["sale_brand_content"] = self.sale_brand.specific.sale_brand_item.all()
        return context

    class Meta:
        verbose_name = "关于我们一级页面"
        verbose_name_plural = "关于我们一级页面"


# 新闻一级页面
class NewsFirstPage(NavMenuItem):
    subpage_types = [
        "home.NewsSecondPage",
    ]

    @property
    def banner_image(self):
        return self.cover_image

    @property
    def news(self):
        # 获取本页面子页面中已发布的页面
        news = NewsSecondPage.objects.live().descendant_of(self)
        order_list = ["-top", "-date"]
        news = news.order_by(*order_list)[1:]
        return news

    @property
    def first_news(self):
        # 获取新闻列表的第一个元素（按时间排列）
        return NewsSecondPage.objects.live().descendant_of(self).order_by("-date")[0]

    def children(self):
        return self.get_children().specific().live()

    def paginate(self, request, *args):
        page = request.GET.get("page")
        paginator = Paginator(self.news, 5)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages

    def get_context(self, request, *args, **kwargs):
        context = super(NewsFirstPage, self).get_context(request)
        news = self.paginate(request, self.news)
        context["news"] = news
        return context

    class Meta:
        verbose_name = "新闻一级页面"
        verbose_name_plural = "新闻一级页面"


# 新闻二级页面
class NewsSecondPage(SubArticlePage):
    subpage_types = []

    @property
    def banner_image(self):
        return self.get_parent().specific.cover_image

    @property
    def name(self):
        return self.author_name

    class Meta:
        verbose_name = "新闻二级页面"


# 产品一级页面,下面产品的种类也是使用的这个模型
class ProductFirstPage(NavMenuItem):
    date = models.DateField("发布日期", blank=True, null=True)
    subpage_types = [
        "home.ProductFirstPage",
        "home.ProductDetailPage"
    ]
    content_panels = NavMenuItem.content_panels + [
        FieldPanel('date'),
    ]

    @property
    def banner_image(self):
        if self.cover_image:
            return self.cover_image
        else:
            cover_image = self.get_parent().specific.cover_image
            return cover_image

    @property
    def green_product(self):
        k = ProductFirstPage.objects.live().filter(title="绿色建筑")
        product = ProductDetailPage.objects.live().child_of(k[0])
        green_product = product.order_by("-date")
        return green_product

    @property
    def clean_product(self):
        k = ProductFirstPage.objects.live().filter(title="清洁能源")
        product = ProductDetailPage.objects.live().child_of(k[0])
        clean_product = product.order_by("-date")
        return clean_product

    @property
    def smart_product(self):
        k = ProductFirstPage.objects.live().filter(title="智慧交通")
        product = ProductDetailPage.objects.live().child_of(k[0])
        smart_product = product.order_by("-date")
        return smart_product

    @property
    def elastic_product(self):
        k = ProductFirstPage.objects.live().filter(title="智能电网")
        product = ProductDetailPage.objects.live().child_of(k[0])
        elastic_product = product.order_by("-date")
        return elastic_product

    @property
    def height_product(self):
        k = ProductFirstPage.objects.live().filter(title="高端设备")
        product = ProductDetailPage.objects.live().child_of(k[1])
        height_product = product.order_by("-date")
        return height_product

    def paginate(self, request, *args):
        page = request.GET.get("page")
        paginator = Paginator(*args, 8)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages

    def get_context(self, request, *args, **kwargs):
        context = super(ProductFirstPage, self).get_context(self)
        green_product = self.paginate(request, self.green_product)
        clean_product = self.paginate(request, self.clean_product)
        smart_product = self.paginate(request, self.smart_product)
        elastic_product = self.paginate(request, self.elastic_product)
        height_product = self.paginate(request, self.height_product)
        context["green_product"] = green_product
        context["clean_product"] = clean_product
        context["smart_product"] = smart_product
        context["elastic_product"] = elastic_product
        context["height_product"] = height_product
        return context

    class Meta:
        verbose_name = "产品一级页面"
        verbose_name_plural = "产品一级页面"


# 产品详情页面
class ProductDetailPage(SubArticlePage):
    subpage_types = []

    @property
    def banner_image(self):
        return self.get_parent().get_parent().specific.cover_image

    class Meta:
        verbose_name = "产品详情页面"


class CaseItem(Orderable, AboutCarouse):
    page = ParentalKey("CaseFirstPage", related_name="case_item")


# 案例一级页面
class CaseFirstPage(NavMenuItem):
    content_panels = Page.content_panels + [
        InlinePanel("case_item", label="图片组")
    ]
    subpage_types = []

    @property
    def banner_image(self):
        return self.cover_image

    def get_context(self, request, *args, **kwargs):
        context = super(CaseFirstPage, self).get_context(request)
        context['swiper_page'] = self.specific.case_item.all()
        return context

    class Meta:
        verbose_name = "案例一级页面"
        verbose_name_plural = "案例一级页面"


# 图片通用二级， 案例展示、公司荣誉墙、专卖店形象、专卖店荣誉
class SimpleImagePage(NavMenuItem):
    date = models.DateField("发布日期")
    notes = models.CharField("英文", blank=True, null=True, max_length=64)
    hans = models.CharField("中文", blank=True, null=True, max_length=64)

    image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="图片"
    )
    subpage_types = []
    content_panels = NavMenuItem.content_panels + [
        FieldPanel("date"),
        FieldPanel("hans"),
        FieldPanel("notes"),
        ImageChooserPanel("image")
    ]

    class Meta:
        verbose_name = "图片通用二级"


class AboutItem(Orderable, AboutCarouse):
    page = ParentalKey("CompanyHonorPage", related_name="about_company_item")


class SaleHonorItem(Orderable, AboutCarouse):
    page = ParentalKey("SaleHonorPage", related_name="sale_honor_item")


class SaleBrandItem(Orderable, AboutCarouse):
    page = ParentalKey("SaleBrandPage", related_name="sale_brand_item")


# 公司荣誉
class CompanyHonorPage(NavMenuItem):
    content_panels = Page.content_panels + [
        InlinePanel("about_company_item", label="图片组")
    ]
    subpage_types = []

    @property
    def banner_image(self):
        banner_image = self.get_parent().specific.cover_image
        return banner_image

    class Meta:
        verbose_name = "公司荣誉墙"


# 专卖店荣誉
class SaleHonorPage(NavMenuItem):
    content_panels = Page.content_panels + [
        InlinePanel("sale_honor_item", label="图片组")
    ]
    subpage_types = []

    @property
    def banner_image(self):
        banner_image = self.get_parent().specific.cover_image
        return banner_image

    class Meta:
        verbose_name = "专卖店荣誉"


# 专卖店形象
class SaleBrandPage(NavMenuItem):
    content_panels = Page.content_panels + [
        InlinePanel("sale_brand_item", label="图片组")
    ]
    subpage_types = []

    @property
    def banner_image(self):
        banner_image = self.get_parent().specific.cover_image
        return banner_image

    class Meta:
        verbose_name = "专卖店形象"


# 专卖店简介
class SalePage(SubArticlePage):
    subpage_types = []

    @property
    def banner_image(self):
        banner_image = self.get_parent().specific.cover_image
        return banner_image

    class Meta:
        verbose_name = "简介"


# 首页轮播图条
class HomePageCarouselItem(Orderable, CarouselItem):
    page = ParentalKey("home.HomePage", related_name="carousel_items")


# 首页
class HomePage(Page):
    sale_parent = models.ForeignKey(
        "wagtailcore.Page",
        verbose_name="专卖店介绍",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="专卖店介绍"
    )
    sale_brand_parent = models.ForeignKey(
        "wagtailcore.Page",
        verbose_name="专卖店形象",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="专卖店形象"
    )
    sale_honor_parent = models.ForeignKey(
        "wagtailcore.Page",
        verbose_name="专卖店荣誉",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="专卖店荣誉"
    )
    company_honor_parent = models.ForeignKey(
        "wagtailcore.Page",
        verbose_name="公司荣誉",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="公司荣誉"
    )
    case_parent = models.ForeignKey(
        "wagtailcore.Page",
        verbose_name="工程案例",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="展示最近的工程案例图片"
    )
    news_parent = models.ForeignKey(
        "wagtailcore.Page",
        verbose_name="专卖店新闻",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="专卖店最新信息动态"
    )
    product_parent = models.ForeignKey(
        "wagtailcore.Page",
        verbose_name="产品中心",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="产品中心信息动态"
    )
    contract_us_parent = models.ForeignKey(
        "wagtailcore.Page",
        verbose_name="联系我们",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="专卖店的联系方式"
    )

    content_panels = Page.content_panels + [
        InlinePanel("carousel_items", label="轮播图片组"),
        PageChooserPanel("case_parent", page_type="home.CaseFirstPage"),
        PageChooserPanel("news_parent", page_type="home.NewsFirstPage"),
        PageChooserPanel("contract_us_parent", page_type="home.FormPage"),
        MultiFieldPanel([
            PageChooserPanel("sale_parent", page_type="home.SalePage"),
            PageChooserPanel("sale_brand_parent", page_type="home.SaleBrandPage"),
            PageChooserPanel("sale_honor_parent", page_type="home.SaleHonorPage"),
            PageChooserPanel("company_honor_parent", page_type="home.CompanyHonorPage"),
        ], heading="关于我们")
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(HomePage, self).get_context(request)
        context["about_us"] = AboutFirstPage.objects.live().all()[0]
        context["company_honor_page"] = self.company_honor_parent.specific.about_company_item.all()[:4]
        context["case_page"] = self.case_parent.specific.case_item.all()[:3]
        context["news_page"] = SubArticlePage.objects.live().descendant_of(self.news_parent).order_by("-date")[:6]
        return context

    subpage_types = [
        "home.AboutFirstPage",
        "home.NewsFirstPage",
        "home.ProductFirstPage",
        "home.FormPage",
        "home.CaseFirstPage",
    ]

    class Meta:
        verbose_name = "主页"


# 设置模块
@register_setting(icon="home")
class SiteInfoSetting(BaseSetting):
    logo = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        verbose_name="商标",
        blank=True,
        null=True,
        related_name="+",
    )
    name = models.CharField("专卖店总站", max_length=256, blank=True)
    tel = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        verbose_name="联系方式",
        blank=True,
        null=True,
        related_name="+",
    )
    left_content = models.CharField("左栏", max_length=64)
    center_content = models.CharField("中栏", max_length=64)
    right_content = models.CharField("右栏", max_length=64)

    panels = [
        ImageChooserPanel("logo"),
        ImageChooserPanel("tel"),
        FieldPanel("name"),
        FieldPanel("left_content"),
        FieldPanel("center_content"),
        FieldPanel("right_content"),
    ]

    class Meta:
        verbose_name = "网站信息"


@register_setting(icon='doc-full')
class AddonScriptsSettings(BaseSetting):
    class Meta:
        verbose_name = '附加功能脚本'

    head = models.TextField(
        verbose_name='head',
        blank=True,
        help_text='添加到head的脚本',
        default=''
    )
    body = models.TextField(
        verbose_name='body',
        blank=True,
        help_text='添加到body的脚本',
        default=''
    )


@register_snippet
class WebSite(models.Model):
    title = models.CharField("网站名称", max_length=32, blank=True, null=True)
    url = models.CharField("URL", max_length=64, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "相关网站"
        verbose_name_plural = "相关网站"


# 提交留言
class FormField(AbstractFormField):
    page = ParentalKey('FormPage', related_name='form_fields', on_delete=models.CASCADE)


class FormPage(AbstractEmailForm):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="封面图片"
    )
    qr_code = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="微信二维码",
    )
    name = models.CharField("联系人", max_length=64, null=True)
    address = models.CharField("地址", max_length=256, null=True)
    tel = models.CharField("电话", max_length=32, null=True)
    fax = models.CharField("传真", max_length=32, null=True)
    QQ = models.IntegerField("QQ", null=True)
    email = models.EmailField("邮箱", max_length=64, null=True)
    thank_you_text = models.TextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        ImageChooserPanel("image"),
        ImageChooserPanel("qr_code"),
        FieldPanel("name"),
        FieldPanel("address"),
        FieldPanel("tel"),
        FieldPanel("fax"),
        FieldPanel("QQ"),
        FieldPanel("email"),
        InlinePanel("form_fields", label="Form fields"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]

    class Meta:
        verbose_name = "在线留言"
