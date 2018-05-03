from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Page
from wagtailmetadata.models import MetadataPageMixin


class Page(MetadataPageMixin, Page):

    class Meta:
        abstract = True

    promote_panels = [
        FieldPanel('search_description'),
        FieldPanel('search_image'),
    ]

    settings_panels = [
        FieldPanel('slug'),
    ]

    def get_template(self, request):
        return 'layouts/{}.html'.format(self._meta.model_name)
