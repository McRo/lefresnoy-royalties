# MONTANT, devise, Taux ARTISTE, fournisseur:titre, fournisseur:PAYS, fournisseur:TVA intra, 
# fournisseur:ADRESSE, redevance:ACTIVITE, diffusion:PERIODE, 
# diffusion:ARTISTE, diffusion:ŒUVRE, demande:Date	demande:N°, demande:Date création, 
# demande:Envoi Mail, demande:Date envoie pdf, PAIEMENT:date, REMARQUES, MAIL,	
# CHORUS:SIRET, chorus:BON DE COMMANDE

from django.db import models
from django_countries.fields import CountryField
from djmoney.models.fields import MoneyField

from django.utils.translation import gettext as _

from decimal import Decimal

from .diffusion import Diffusion, Place

# demande:Date	demande:N°, demande:Date création, 
# demande:Envoi Mail, demande:Date envoie pdf, PAIEMENT:date, REMARQUES, MAIL,	
# CHORUS:SIRET, chorus:BON DE COMMANDE


class Artist(models.Model):
    name = models.CharField(max_length=255, blank=False)
    contact = models.CharField(max_length=255, null=True, blank=False)
    is_teacher = models.BooleanField(default=False, help_text="Professeur ?")

    def __str__(self):
        return "{} ({})".format(self.name, self.contact if self.contact else "contact manquant")


class Artwork(models.Model):
    title = models.CharField(max_length=255, blank=False)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} de {self.artist}"
    

class Supplier(models.Model):
    # fournisseur
    title = models.CharField(max_length=255)
    address = models.TextField(null=True, blank=True)
    country = CountryField(blank=True)
    tva_intra = models.CharField(max_length=50, blank=True)
    siret = models.CharField(max_length=100, blank=True)
    contact = models.CharField(max_length=255, null=True, blank=False)

    def __str__(self):
        return "{} ({})".format(self.title, self.country)


class Payment(models.Model):

    number = models.CharField(max_length=50, blank=True, help_text="Numéro")
    purchase_order = models.CharField(max_length=10, null=True, blank=True, help_text="Bon de commande")
    
    billing_date = models.DateField(help_text="Date de facturation", null=True, blank=True)
    billing_send_date = models.DateField(help_text="Date d'envoi de la facture", null=True, blank=True)
    
    payment_date = models.DateField(help_text="Date de paiement", null=True, blank=True)

    def __str__(self):
        return "{}-{} paiement pour {}".format(self.number, self.payment_date.strftime("%B %Y") if self.payment_date else "??" ,self.royalty.diffusion.artist if self.royalty else "")


class Royalty(models.Model):
    class Meta:
        verbose_name_plural = "royalties"

    activity = models.CharField(max_length=255, blank=True, null=True, help_text="Diffusion, refacturation, ...")
    # $$
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,)
    with_tax = models.BooleanField(default=True, help_text="HT or TTC")
    money = MoneyField(max_digits=14, decimal_places=2, null=True, default_currency='EUR')
    # 
    diffusion = models.ForeignKey(Diffusion, null=True, blank=True, on_delete=models.CASCADE)
    artist_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Pourcentage artiste" ,help_text="%")

    supplier = models.ForeignKey(Supplier, null=True, blank=True, related_name='royalties', on_delete=models.CASCADE)
    # 
    validation_date = models.DateField(help_text="Date à laquelle toutes les données sont remplies", null=True, blank=True)
    # comptabilite
    payment = models.OneToOneField(Payment, null=True, blank=True, on_delete=models.CASCADE)
    # free remark
    remark = models.TextField(null=True, blank=True)
    # Dates of creation
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.activity} - {self.supplier} {self.diffusion.artist.name} {self.amount} {self.money.currency }"
    


class Notification(models.Model):
    """
    Status of automations
    """
    created_on = models.DateTimeField(auto_now_add=True)
    # type : mail (SMS?Whatsapp?)
    type = models.CharField(max_length=50)
    # destinataire
    recipient = models.CharField(max_length=150)
    # status : sended / error
    status = models.CharField(max_length=50)
    # content of message
    content = models.TextField(null=True, blank=False)
    # royalty subject
    royalty = models.ForeignKey(Royalty, related_name='notifications', on_delete=models.CASCADE, null=True, blank=False)
    
    def __str__(self):
        return "{}-{} à {} pour ".format(self.type, self.status, self.recipient, self.royalty.number)
