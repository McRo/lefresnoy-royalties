from django import forms
from django.contrib.auth import forms as auth_forms
from django.utils.translation import gettext_lazy as _

from tapeforms.contrib.bootstrap import Bootstrap5TapeformMixin

from ..models import User


class PlaceholderFormMixin(Bootstrap5TapeformMixin):
    field_label_css_class = 'sr-only'

    def apply_widget_options(self, field_name):
        field = self.fields[field_name]
        # add a placeholder attribute with the label
        field.widget.attrs['placeholder'] = field.label


class AuthenticationForm(PlaceholderFormMixin, auth_forms.AuthenticationForm):
    pass
