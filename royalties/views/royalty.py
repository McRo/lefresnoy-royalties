import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect, reverse

from django.views.generic import TemplateView
from django.views import View, generic


from royalties.forms import RoyaltyForm, RoyaltyCreateForm, DiffusionForm, PaymentForm, SupplierForm
from royalties.models import Royalty

class RoyaltyListView(LoginRequiredMixin, generic.ListView):
    template_name = 'pages/royalties.html'
    model = Royalty
    context_object_name = 'royalties'

    def get_queryset(self):
        new_context = Royalty.objects.all()
        # try to get homemade filter
        filter_val = self.request.GET.get('filter', None)
        print(filter_val)
        if filter_val == "todo" :
            now = datetime.datetime.now()
            new_context = Royalty.objects.filter(
                validation_date__lt=now, payment__payment_date__isnull=True
            ).order_by("validation_date")            
        return new_context



class RoyaltyDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'pages/royalty.html'
    model = Royalty
    context_object_name = 'royalty'


class RoyaltyUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'pages/royalty-edit.html'
    model = Royalty
    form_class = RoyaltyForm
    # success_url = "/thanks/"
    # fields = '__all__'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, "Sauvegarde OK")
        # messages.success(request, "Sauvegarde OK")
        return reverse("royalty-detail", kwargs={"pk":self.kwargs.get('pk')})

    

def update_royalty(request, pk):
    
    r = Royalty.objects.get(pk=pk)

    if request.method == 'POST':
        royalty_form = RoyaltyForm(request.POST, instance=r, prefix='royalty')

        if all([royalty_form.is_valid(),]):
            royalty_form.save()

            messages.success(request, "Sauvegarde OK")
            #  return redirect(request.path)
            return redirect("royalty-detail", pk=pk)


    else:
        royalty_form = RoyaltyForm(instance=r, prefix='royalty')

    context= {"royalty":royalty_form, }

    return render(
        request,
        "pages/royalty-edit.html",
        context,
    )


def create_royalty(request,):

    if request.method == 'POST':
        royalty_form = RoyaltyForm(request.POST, prefix='royalty')
        diffusion_form = DiffusionForm(request.POST, prefix='diffusion')
        supplier_form = SupplierForm(request.POST, prefix='supplier')
        payment_form = PaymentForm(request.POST, prefix='payment')

        if all([royalty_form.is_valid(),
                diffusion_form.is_valid(),
                supplier_form.is_valid(), 
                payment_form.is_valid()]):
            new_diffusion = diffusion_form.save()
            new_supplier = supplier_form.save()
            new_payment = payment_form.save()

            new_royalty = royalty_form.save()
            new_royalty.supplier=new_supplier
            new_royalty.diffusion=new_diffusion
            new_royalty.payment=new_payment

            new_royalty.save()


            print(new_supplier)

            messages.success(request, "Sauvegarde OK")
            #  return redirect(request.path)
            return redirect("royalty-detail", pk=new_royalty.pk)

    else:
        royalty_form = RoyaltyForm(prefix='royalty')
        diffusion_form = DiffusionForm(prefix='diffusion')
        supplier_form = SupplierForm(prefix='supplier')
        payment_form = PaymentForm(prefix='payment')

        all_form = RoyaltyCreateForm(prefix='all')


    context= {"royalty":royalty_form, "diffusion":diffusion_form, 
              "supplier": supplier_form, 
              "payment":payment_form, "all":all_form }
    return render(
        request,
        "pages/royalty-create.html",
        context,
    )



    
