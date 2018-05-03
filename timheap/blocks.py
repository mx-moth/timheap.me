from functools import total_ordering

from django.template.loader import render_to_string
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_all_lexers, get_lexer_by_name
from wagtail.core import blocks
from wagtail.core.rich_text import expand_db_html
from wagtail.images.blocks import ImageChooserBlock

from . import rich_text


class StreamBlock(blocks.StreamBlock):
    def render_list_member(self, block_type_name, value, prefix, index, errors=None, id=None):
        """
        Render the HTML for a single list item. This consists of an <li>
        wrapper, hidden fields to manage ID/deleted state/type, delete/reorder
        buttons, and the child block's own HTML.
        """
        child_block = self.child_blocks[block_type_name]
        child = child_block.bind(value, prefix="%s-value" % prefix, errors=errors)
        return render_to_string('wagtailadmin/block_forms/stream_member.html', {
            'child_blocks': sorted(self.child_blocks.values(), key=lambda child_block: child_block.meta.group),
            'block_type_name': block_type_name,
            'prefix': prefix,
            'child': child,
            'index': index,
            'block_id': id,
        })

    def render_basic(self, value, context=None):
        content = '\n'.join(child.render(context=context) for child in value)
        return mark_safe('''<div class="rich-text">{}</div>'''.format(content))


@total_ordering
class Group(object):
    """
    Named structblock groups, with sort order
    """

    def __init__(self, order, label):
        self.order = order
        self.label = label

    def __str__(self):
        return self.label

    def __repr__(self):
        return "<Group: %s>" % self.label

    def __lt__(self, other):
        if not isinstance(other, Group):
            return NotImplemented
        return self.order < other.order

    def __eq__(self, other):
        if not isinstance(other, Group):
            return NotImplemented
        return self.order == other.order


CONTENT = Group(100, 'Content')
EMBEDS = Group(200, 'Embeds')


class RichTextBlock(blocks.RichTextBlock):
    def render_basic(self, value, context=None):
        return expand_db_html(value.source)


class HeadingBlock(blocks.CharBlock):
    class Meta:
        icon = 'title'

    def __init__(self, size, **kwargs):
        super().__init__(**kwargs)
        self.size = size
        self.meta.classname = 'block-heading block-heading--h{}'.format(size)

    def render_basic(self, value, context=None):
        return format_html('<h{size}>{text}</h{size}>',
                           size=self.size, text=value)


class HorizontalRuleBlock(blocks.StaticBlock):
    class Meta:
        icon = 'horizontalrule'
        template = 'blocks/hr.html'

    def render_form(self, value, prefix='', errors=None):
        return mark_safe('<hr class="block-hr">')


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    caption = RichTextBlock(
        features=rich_text.INLINE + rich_text.LINKS,
        required=False)

    class Meta:
        icon = 'image'
        template = 'blocks/image.html'


class InlineImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    align = blocks.ChoiceBlock(choices=[
        ('left', "Left"),
        ('right', "Right"),
    ])

    class Meta:
        icon = 'image'
        template = 'blocks/inline-image.html'


class CodeBlock(blocks.StructBlock):
    language = blocks.ChoiceBlock(choices=[
        (alias[0], name) for name, alias, _, _ in get_all_lexers()
    ])
    code = blocks.TextBlock(classname='input-monospace')
    line_numbers = blocks.BooleanBlock(required=False)

    class Meta:
        icon = 'code'

    def render_basic(self, value, context=None):
        lexer = get_lexer_by_name(value['language'])
        formatter = HtmlFormatter(linenos=value['line_numbers'])
        return mark_safe(highlight(value['code'], lexer, formatter))


class ContentBlocks(StreamBlock):
    h2 = HeadingBlock(2, group=CONTENT, label="Heading")
    h3 = HeadingBlock(3, group=CONTENT, label="Subheading")
    h4 = HeadingBlock(4, group=CONTENT, label="Subsubheading")
    text = RichTextBlock(
        icon='pilcrow',
        features=rich_text.INLINE + rich_text.LINKS + rich_text.LISTS,
        group=CONTENT,
    )
    hr = HorizontalRuleBlock(group=CONTENT, label="Horizontal rule")

    image = ImageBlock(group=EMBEDS)
    inline_image = InlineImageBlock(group=EMBEDS)
    code = CodeBlock(group=EMBEDS)
