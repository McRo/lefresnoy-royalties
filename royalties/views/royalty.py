from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views import View, generic

from royalties.models import Royalty

class ShowRoyaltiesView(LoginRequiredMixin, generic.ListView):
    template_name = 'pages/royalties.html'
    model = Royalty
    context_object_name = 'royalties'
