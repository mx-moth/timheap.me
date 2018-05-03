from wagtail.core import blocks

from .blocks import StreamBlock


class URLBlock(blocks.StructBlock):
    url = blocks.URLBlock()
    text = blocks.CharBlock()

    class Meta:
        icon = 'link'


class MenuBlocks(StreamBlock):
    page = blocks.PageChooserBlock()
    url = URLBlock()


class HeaderMenuBlocks(MenuBlocks):
    class Meta:
        template = 'blocks/menu.html'
