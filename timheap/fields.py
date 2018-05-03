from wagtail.core.fields import StreamField


class StreamField(StreamField):
    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        args = [[]]  # Don't keep blocks around for the migration
        return name, path, args, kwargs
