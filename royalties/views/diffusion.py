from django.views.generic import DetailView, UpdateView, ListView, CreateView
from django.urls import reverse
from django.contrib import messages

from royalties.models import Diffusion
from royalties.forms import DiffusionForm

from django.contrib.auth.mixins import LoginRequiredMixin


class DiffusionUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'pages/diffusion-edit.html'
    model = Diffusion
    form_class = DiffusionForm
    # success_url = "/thanks/"
    # fields = '__all__'

    # add url back

    def get_initial(self):
        initial_values = super().get_initial()
        print(self.object.start)
        # replace ID by his place's title
        if self.object.place:
            initial_values['place'] = self.object.place.title
        return initial_values

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
    

class DiffusionListView(LoginRequiredMixin, ListView):
    template_name = 'pages/diffusion-list.html'
    model = Diffusion

    def get_ordering(self):
        ordering = self.request.GET.get('o', 'start')
        # validate ordering here
        return ordering


class DiffusionCreateView(LoginRequiredMixin, CreateView):
    template_name = 'pages/diffusion-create.html'
    model = Diffusion
    form_class = DiffusionForm

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, "Creation OK")
        # back to diffusion list
        return reverse("diffusion-list")


class DiffusionDetailView(LoginRequiredMixin, DetailView):
    template_name = 'pages/diffusion-detail.html'
    model = Diffusion
    form_class = DiffusionForm
