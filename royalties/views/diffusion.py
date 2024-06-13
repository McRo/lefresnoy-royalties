from django.views.generic import DetailView, UpdateView
from django.urls import reverse
from django.contrib import messages

from royalties.models import Diffusion
from royalties.forms import DiffusionForm


class DiffusionUpdateView(UpdateView):
    template_name = 'pages/diffusion-edit.html'
    model = Diffusion
    form_class = DiffusionForm
    # success_url = "/thanks/"
    # fields = '__all__'

    # add url back

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        royalty = self.request.GET.get('royalty', None)
        if royalty:
            context['back'] = reverse("royalty-detail", kwargs={"pk":royalty})
        return context
    
    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, "Sauvegarde OK")
        royalty = self.request.GET.get('royalty', None)
        if royalty:
            return reverse("royalty-detail", kwargs={"pk":royalty})
        return self.request.path
    