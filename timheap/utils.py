from django.utils.functional import lazy
from django.utils.html import format_html


def lazy_format_html(value, kwargs_fn):
    """
    A lazy form of format_html that gathers format kwargs on demand from
    a callable. Useful for making help text with URLs. Use like:

    .. code-block:: python

        lazy_format_html(
            'Frobnicate the quux. <a href="{href}">Read more</a>',
            lambda: {'href': reverse('quux:frobincate')})
    """
    return lazy(lambda: format_html(value, **kwargs_fn()), str)()
