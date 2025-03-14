from django.utils.functional import cached_property, lazy
from wagtail import VERSION as WAGTAIL_VERSION

if WAGTAIL_VERSION[0] >= 3:
    from wagtail.blocks import ChooserBlock
    from wagtail.coreutils import resolve_model_string
else:
    from wagtail.core.blocks import ChooserBlock
    from wagtail.core.utils import resolve_model_string

from . import registry
from .widgets import AdminModelChooser


class ModelChooserBlock(ChooserBlock):
    def __init__(self, target_model, filter_name=None, **kwargs):
        super(ModelChooserBlock, self).__init__(**kwargs)
        self._target_model = target_model

        self.filter_name = filter_name

        if self.meta.icon == 'placeholder':
            # Get the icon from the chooser.
            # The chooser may not have been registered yet, depending upon
            # import orders and things, so get the icon lazily
            self.meta.icon = lazy(lambda: self.chooser.icon, str)()

    @cached_property
    def target_model(self):
        return resolve_model_string(self._target_model)

    @cached_property
    def widget(self):
        return AdminModelChooser(self.target_model,
                                 filter_name=self.filter_name)

    @cached_property
    def chooser(self):
        return registry.choosers[self.target_model]

    def get_form_state(self, value):
        return self.widget.get_value_data(value)

    def deconstruct(self):
        name, args, kwargs = super(ModelChooserBlock, self).deconstruct()

        if args:
            args = args[1:]  # Remove the args target_model

        kwargs['target_model'] = self.target_model._meta.label_lower
        return name, args, kwargs

    class Meta:
        icon = "placeholder"
