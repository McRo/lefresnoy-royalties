import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect, reverse

from django.views.generic import TemplateView
from django.views import View, generic


from royalties.forms import RoyaltyForm, RoyaltyCreateForm, DiffusionForm, PaymentForm, SupplierForm
from royalties.models import Royalty
from royalties.models import Diffusion

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
        diffusion_id = request.POST['all-diffusion']      

        print("diffusion", diffusion_id)  
        
        supplier_form = SupplierForm(request.POST, prefix='supplier')
        supplier_id = request.POST['all-supplier']

        print("supplier_id", supplier_id)
        
        payment_form = PaymentForm(request.POST, prefix='payment')

        if all([diffusion_id,
                supplier_id,
                royalty_form.is_valid(), 
                payment_form.is_valid()]):
            

            # create new royalty from FORM
            royalty_create_form = RoyaltyCreateForm(request.POST, prefix='royalty')
            # save it 
            royalty = royalty_create_form.save(commit=False)
            # set ids from select
            royalty.diffusion_id = diffusion_id
            royalty.supplier_id = supplier_id
            # set onetoone
            payment = payment_form.save()
            royalty.payment_id = payment.id
            # save
            royalty.save()
            
            messages.success(request, "Sauvegarde OK")
            #  return redirect(request.path)
            return redirect("royalty-detail", pk=royalty.pk)
            

    else:
        royalty_form = RoyaltyForm(prefix='royalty')
        # Create a datalist for all diffusions
        diffusion_form = DiffusionForm(prefix='diffusion')

        supplier_form = SupplierForm(prefix='supplier')
        payment_form = PaymentForm(prefix='payment')

        all_form = RoyaltyCreateForm(prefix='all')

    context= {"royalty":royalty_form, "diffusion":diffusion_form, 
              "supplier": supplier_form, 
              "payment":payment_form, 
              "all":all_form 
              }
    return render(
        request,
        "pages/royalty-create.html",
        context,
    )



    
