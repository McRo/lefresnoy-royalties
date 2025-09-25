from django.db import models
from django_countries.fields import CountryField

from django.utils.translation import gettext as _


class Place(models.Model):
    title = models.CharField(max_length=255, blank=True, help_text="Nom du lieu")

    address = models.CharField(max_length=255, blank=True, help_text="Adresse")
    city = models.CharField(max_length=255, blank=True, help_text="Ville")
    country = models.CharField(max_length=255, blank=True, help_text="Pays")

    lon = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.country})"


class Diffusion(models.Model):
    title = models.CharField(max_length=255, blank=True, help_text="Titre de la diffusion")

    place = models.ForeignKey(Place, null=True, blank=True, on_delete=models.SET_NULL)

    start = models.DateField(blank=False, null=False)
    end = models.DateField(blank=True, null=True)

    artist = models.ForeignKey("Artist", on_delete=models.CASCADE)
    artwork = models.ForeignKey("Artwork", on_delete=models.CASCADE)

    def __str__(self):
        date = "Le "+self.start.strftime("%w %B %Y")
        if not self.end or self.start == self.end:
            date = _("Le "+self.start.strftime("%w %B %Y"))
        elif self.start.strftime("%B %Y") == self.end.strftime("%B %Y"):
            date = "Du "+self.start.strftime("%w")+" au "+ self.end.strftime("%w %B %Y")
        else:
            date = "Du "+self.start.strftime("%w %B")+" au "+ self.end.strftime("%w %B %Y")
        title = ""+self.title if self.title else ""
        return "{} au {} - {} {}".format(title.capitalize(), self.place, date, self.artwork)