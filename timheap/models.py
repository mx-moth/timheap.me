from django.db import models
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting

from .blocks import ContentBlocks
from .fields import StreamField
from .menus import HeaderMenuBlocks
from .page import Page


class ContentPage(Page):
    content = StreamField(ContentBlocks())

    content_panels = Page.content_panels + [
        StreamFieldPanel('content')
    ]


@register_setting
class SiteSettings(BaseSetting):
    google_analytics_code = models.CharField(max_length=30, blank=True)


@register_setting(icon='link')
class Menus(BaseSetting):
    header = StreamField(HeaderMenuBlocks())

    panels = [
        StreamFieldPanel('header'),
    ]
