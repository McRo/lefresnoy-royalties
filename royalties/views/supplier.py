from django.views.generic import DetailView, UpdateView
from django.urls import reverse
from django.contrib import messages

from royalties.models import Supplier
from royalties.forms import SupplierForm


class SupplierUpdateView(UpdateView):
    template_name = 'pages/supplier-edit.html'
    model = Supplier
    form_class = SupplierForm
    # success_url = "/thanks/"
    # fields = '__all__'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, "Sauvegarde OK")
        royalty = self.request.GET.get('royalty', None)
        if next:
            return reverse("royalty-detail", kwargs={"pk":royalty})
        return self.request.path