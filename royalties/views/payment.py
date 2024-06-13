from django.views.generic import DetailView, UpdateView
from django.urls import reverse
from django.contrib import messages

from royalties.models import Payment
from royalties.forms import PaymentForm


class PaymentUpdateView(UpdateView):
    template_name = 'pages/payment-edit.html'
    model = Payment
    form_class = PaymentForm
    # success_url = "/thanks/"
    # fields = '__all__'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, "Sauvegarde OK")
        return self.request.path