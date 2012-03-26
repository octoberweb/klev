from apps.banners.models import Banners
from django import template

register = template.Library()

@register.inclusion_tag("banners/banner_right.html")
def get_right_banner():
    banners = Banners.items.all()
    banners = banners.order_by('?')
    if banners:
        return {'banner': banners[0]}
    else: return {'banner': False}


@register.inclusion_tag("banner_right.html")
def get_left_banner():
    banner = Banners.objects.order_by('-order').filter(left=True, show=True)
    if banner:
        return {'banner': banner[0]}
    else: return {'banner': False}


@register.inclusion_tag("banner_footer.html")
def get_footer_banner():
    banner = Banners.objects.order_by('-order').exclude(right=True).exclude(left=True).filter(show=True)
    if banner:
        return {'banner': banner[0]}
    else: return {'banner': False}
