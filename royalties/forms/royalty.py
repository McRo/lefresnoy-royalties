from django import forms
from tapeforms.mixins import TapeformMixin
from tapeforms.contrib.bootstrap import Bootstrap5TapeformMixin
from django_select2 import forms as s2forms
from royalties.models import Artist, Artwork, Diffusion, Supplier, Payment, Royalty, Notification

from django.forms.widgets import TextInput
from django.utils.safestring import mark_safe



class DatalistTextInput(TextInput):
    def __init__(self, attrs=None):
        super().__init__( attrs)
        if 'list' not in self.attrs or 'datalist' not in self.attrs:
            raise ValueError(
              'DatalistTextInput widget is missing required attrs "list" or "datalist"')
        self.datalist_name = self.attrs['list']

        # pop datalist for use by our render method. 
        # its a pseudo-attr rather than an actual one
        self.datalist = self.attrs.pop('datalist') 

    def render(self, **kwargs):
        part1 = super().render( **kwargs)
        opts = ' '.join(
            [ f'<option>{x}</option>' for x in self.datalist ]
        )
        part2 = f'<datalist id="{self.datalist_name}">{opts}</datalist>'
        return part1 + mark_safe( part2)


class PaymentForm(Bootstrap5TapeformMixin, forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'
    
    payment_date = billing_date = billing_send_date = forms.DateField(
        required=False,
        widget=forms.SelectDateWidget(empty_label="---")
    )


class ArtistForm(Bootstrap5TapeformMixin, forms.ModelForm):
    class Meta:
        model = Artist
        fields = '__all__'


class ArtworkForm(Bootstrap5TapeformMixin, forms.ModelForm):
    class Meta:
        model = Artwork
        fields = '__all__'


class DiffusionForm(Bootstrap5TapeformMixin, forms.ModelForm):
    class Meta:
        model = Diffusion
        fields = '__all__'


class ArtworkForm(Bootstrap5TapeformMixin, forms.ModelForm):
    class Meta:
        model = Artwork
        fields = '__all__'



class SupplierForm(Bootstrap5TapeformMixin, forms.ModelForm):

    class Meta:
        model = Supplier
        fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     super(SupplierForm, self).__init__(*args, **kwargs)
    #     for f in self.fields:
    #         self.fields[f].widget.attrs.update({'class': 'coucou'})


class RoyaltyForm(Bootstrap5TapeformMixin, forms.ModelForm):
    class Meta:
        model = Royalty
        # fields = '__all__'
        fields = ('activity', 'money', 'with_tax', 'artist_rate', 'validation_date', 'remark',  )

    activity = forms.CharField(
        widget = DatalistTextInput( attrs={
            'autocomplete': 'off',
            'list':'foolist',
            'datalist': Royalty.objects.exclude(activity="").distinct().order_by('activity').values_list('activity', flat=True)
            }
    ))

    with_tax = forms.ChoiceField(widget=forms.RadioSelect, choices=((True, 'TTC'), (False, 'HT')),)


class RoyaltyCreateForm(Bootstrap5TapeformMixin, forms.ModelForm):
    class Meta:
        model = Royalty
        fields = '__all__'
        # exclude = ('payment',)
