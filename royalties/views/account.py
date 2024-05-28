from django.conf import settings
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _


from ..forms.account import (
    AuthenticationForm,
)


class LoginView(auth_views.LoginView):
    """
    Logs a user in or link to registration and password reset.
    """

    authentication_form = AuthenticationForm
    template_name = 'account/login.html'
    extra_context = {'title': _("Sign in")}


class LogoutView(auth_views.LogoutView):
    """
    Logs the user out.
    """
    template_name = 'account/logout.html'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, gettext("You have been logged out."))
        return response

