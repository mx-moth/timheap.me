from django import template
from django.conf import settings
from wagtail.core.models import Page
from wagtail.core.templatetags.wagtailcore_tags import pageurl

register = template.Library()


@register.simple_tag(takes_context=True, name='pageurl')
def sensible_pageurl(context, page, fallback='#'):
    """
    An improved {% pageurl %} that returns a fallback URL (default "#") when
    ``page`` is ``None``, unpublished, or inaccessible via a URL, rather than
    crashing, returning a URL that will 404, or returning ``None``
    respectively.
    """
    if page is None or not isinstance(page, Page) or not page.live:
        return fallback

    url = pageurl(context, page)

    if url is None:
        return fallback
    else:
        return url


class PageUrlBlockNode(template.Node):
    """
    A block that only renders if a Wagtail page has a URL. If a page is None,
    is not live, or is not accessible via a URL, the page does not have a URL:
    .. code-block:: html+django
        {% pageurlblock some_page as href %}
            <a href="{{ href }}">some_page.title</a>
        {% empty %}
            <span>No page link for you!</span>
        {% endpageurlblock %}
    The {% empty %} block is optional. If it is not present, nothing will be
    rendered when the page url is empty.
    """
    start_tag = 'pageurlblock'
    empty_tag = 'empty'
    end_tag = 'end' + start_tag

    def __init__(self, href_nodelist, empty_nodelist, page_var, href_name):
        self.href_nodelist = href_nodelist
        self.empty_nodelist = empty_nodelist or template.NodeList()
        self.page_var = page_var
        self.href_name = href_name

    def render(self, context):
        """
        Render href_nodelist if the page has a URL, else render empty_nodelist.
        """
        page = self.page_var.resolve(context)
        href = sensible_pageurl(context, page, fallback=None)
        if href is not None:
            with context.push():
                context[self.href_name] = href
                return self.href_nodelist.render(context)
        else:
            return self.empty_nodelist.render(context)

    @classmethod
    def parse(cls, parser, token):
        """Parse a {% pageurlblock %} and make a PageUrlBlockNode instance."""
        usage = 'Use like {{% {} page as var_name %}}"'.format(cls.start_tag)

        bits = token.split_contents()
        if len(bits) != 4:
            raise template.TemplateSyntaxError(usage)
        if bits[-2] != 'as':
            raise template.TemplateSyntaxError(usage)
        _pageurlblock, page_var, _as, href_name = bits

        href_nodelist = parser.parse([cls.empty_tag, cls.end_tag])
        token = parser.next_token()
        if token.contents == cls.empty_tag:
            empty_nodelist = parser.parse([cls.end_tag])
            parser.delete_first_token()
        else:
            empty_nodelist = None

        return cls(href_nodelist, empty_nodelist,
                   parser.compile_filter(page_var), href_name)


register.tag(PageUrlBlockNode.start_tag, PageUrlBlockNode.parse)


@register.simple_tag(takes_context=True)
def use_google_analytics(context):
    """
    Should Google Analytics be enabled?. It is disabled for administrators,
    when pages are being previewed, or if the Google Analytics code is not
    set.
    """
    if settings.DEBUG:
        return False

    request = context['request']
    if getattr(request, 'is_preview', False):
        return False

    user = request.user
    if user.is_staff or user.is_superuser:
        return False

    site_settings = context['settings']['timheap']['sitesettings']
    if not site_settings.google_analytics_code:
        return False

    return True
