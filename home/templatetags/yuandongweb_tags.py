from django import template
from home.models import SiteInfoSetting
from wagtail.core.models import Page
from home.models import AboutFirstPage
from home import models

register = template.Library()


@register.simple_tag(takes_context=True)
def get_site_root(context, calling_page):
    return calling_page.get_site().root_page


def has_menu_children(page):
    return page.get_children().live().in_menu().exists()


@register.inclusion_tag("home/tags/header.html", takes_context=True)
def header_nav(context, parent=None, calling_page=None):
    if calling_page:
        site = calling_page.get_site()
    else:
        site = context["request"].site
    settings = SiteInfoSetting.for_site(site)
    if not parent:
        parent = site.root_page
    menuitems = parent.get_children().live().in_menu()

    for menuitem in menuitems:
        menuitem.show_dropdown = has_menu_children(menuitem)

    return {
        'calling_page': calling_page,
        'menuitems': menuitems,
        'root_page': site.root_page,
        'logo_img': settings.logo,
        'tel_img': settings.tel,
        'name': settings.name,
        # 在模板中用到pageurl标签，它需要此参数
        'request': context['request'],
    }


# 脚本
@register.inclusion_tag("home/tags/footer.html", takes_context=True)
def foot_nav(context, parent=None, calling_page=None):
    if calling_page:
        site = calling_page.get_site()
    else:
        site = context["request"].site
    about_us = AboutFirstPage.objects.descendant_of(site.root_page)[0]
    sale = models.SalePage.objects.descendant_of(site.root_page)[0]
    company = models.CompanyHonorPage.objects.descendant_of(site.root_page)[0]
    sale_honor = models.SaleHonorPage.objects.descendant_of(site.root_page)[0]
    sale_brand = models.SaleBrandPage.objects.descendant_of(site.root_page)[0]
    product = models.ProductFirstPage.objects.live().get(title="产品中心")
    news = models.NewsFirstPage.objects.live().descendant_of(site.root_page)[0]
    contract = models.FormPage.objects.live().all()[0]
    foot = SiteInfoSetting.for_site(site)
    websites = models.WebSite.objects.all()
    return {
        "about_us": about_us,
        "sale": sale,
        "company": company,
        "sale_honor": sale_honor,
        "sale_brand": sale_brand,
        "product": product,
        "news": news,
        "left": foot.left_content,
        "center": foot.center_content,
        "right": foot.right_content,
        "station": foot.name,
        "tel": contract.tel,
        'websites': websites,
    }


@register.inclusion_tag("home/tags/dropdown.html", takes_context=True)
def header_dropdown(context, parent, parent_specific, submenu=False):
    menuitems_children = parent.get_children()
    menuitems_children = menuitems_children.live().in_menu()
    for menuitem in menuitems_children:
        menuitem.show_dropdown = has_menu_children(menuitem)
    return {
        'parent': parent,
        'parent_specific': parent_specific,
        'submenu': submenu,
        'menuitems_children': menuitems_children,
        # 在模板中用到pageurl标签，它需要此参数
        'request': context['request'],
    }


# 面包屑导航
@register.inclusion_tag('home/tags/breadcrumbs.html', takes_context=True)
def breadcrumbs(context, page):
    self = context.get('self')
    if self is None or self.depth < 2:
        ancestors = ()
    else:
        ancestors = Page.objects.ancestor_of(
            self, inclusive=True,
        ).filter(depth__gt=2)
    return {
        "ancestors": ancestors,
        "page": page,
        "request": context["request"]
    }


# 二级导航
@register.inclusion_tag("home/tags/product_sub_nav.html", takes_context=True)
def sub_nav(context, menu_pages):
    request = context["request"]
    return {
        "menu_pages": menu_pages,
        "request": request
    }
