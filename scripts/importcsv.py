import csv, datetime, urllib, argparse

import dateutil.parser
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from django.contrib.auth.models import User

from geopy.geocoders import Nominatim

from slugify import slugify
import dateutil
from decimal import Decimal
from djmoney.money import Money

from royalties.models import (
    Artist,
    Artwork,
    Diffusion,
    Place,
    Supplier,
    Royalty,
    Payment,
    Notification,
)


def get_or_create(model, attr, save=True):
    # get (or create) object with attributes (without exeption)
    created = False
    try:
        instance = model.objects.get(**attr)
    except Exception:
        instance = model(**attr)
        created = True
        # save
        if save:
            instance.save()
    return [instance, created]


def guessDate(date_str, default=None):
    if date_str != "":
        date_str = "01/05/2024" if date_str == "mai" else date_str
        date_str = "01/03/2024" if date_str == "mars" else date_str
        date_str = "01/02/2024" if date_str == "fevrier" or date_str == "février" else date_str
        date_str = "01/01/2024" if date_str == "janvier" else date_str
        date_str = "01/07/2024" if date_str == "S2 2023" or date_str == "S2/2023" else date_str
        multidates = ("-", "au", "+")
        for sep in multidates:
            if sep in date_str:
                print(date_str)
                date_split = date_str.split(sep)
                if len(date_split[0]) > 2:
                    date_str = date_split[0]
                elif "/" in date_split[1]:
                    date_str = date_split[0] + "/" + date_split[1].split("/")[1]
                date_str += "/2024"
        try:
            date = dateutil.parser.parse(date_str)
            print("trouvé : " + str(date))
            return date
        except Exception as e:
            print(e)
            print("Date non reconnu : " + date_str)
            new_date_str = input("Entrez une date : ")
            if new_date_str != "":
                return guessDate(new_date_str)
    return default


def getCityFromGeo(geo_data):
    fields = ["city", "town", "village"]
    for f in fields:
        if f in geo_data:
            return geo_data[f]
    return None


guess_location_cache = {}
# Try to get location (with geopy) ask to precise location when not find it
def guessLocation(address, new_address=False):
    """
    Guesses the location of an address using a geocoding service.

    Args:
        address: The primary address to geocode.
        new_address: An optional alternative address for loop functtion call and keep initial address.

    Returns:
        The geocoded location object, or False if the location could not be determined.
    """

    # search for cache first
    if address in guess_location_cache:
        return guess_location_cache[address]
    # why not ?
    if new_address in guess_location_cache:
        return guess_location_cache[new_address]
    
    address_search = new_address or address
    
    geolocator = Nominatim(user_agent="place_create_app")
    location = geolocator.geocode(address_search or address, addressdetails=True)

    if not location:
        print(f"L'adresse n'a pas pu être identifiée, {address_search} ({address})")
        address_modified = input("Donnez un adresse plus simple ou passez cette étape : ")
        if len(address_modified) > 3:
            return guessLocation(address, new_address=address_modified)
        else:
            return False

    guess_location_cache[address] = location
    if new_address:
        guess_location_cache[new_address] = location
    return location


def populateDB(data_line):
    name = data_line["name"].title()
    artist, created = Artist.objects.get_or_create(name=name)
    # if(created):
    #     artist.contact =
    artwork, created = Artwork.objects.get_or_create(title=data_line["artwork_title"], artist=artist)
    # PLACE
    place, created = get_or_create(Place, {'title': data_line["supplier_title"]}, False)
    if created:
        location = guessLocation(data_line["supplier_address"])
        if location:
            place.address = location.raw["display_name"]
            place.city = getCityFromGeo(location.raw['address'])
            place.country = location.raw['address']["country"]
            place.lon = location.raw["lon"]
            place.lat = location.raw["lat"]
        else:
            print("Location indisponible pour {})".format(data_line["supplier_title"]))   
        place.save()

    # DIFF
    diff_date_start = guessDate(data_line["diff_start"], datetime.datetime.now())
    diffusion, created = Diffusion.objects.get_or_create(
        title=data_line["supplier_title"], start=diff_date_start, artist=artist, artwork=artwork, place=place
    )
    # SUPPLIER
    supplier, created = Supplier.objects.get_or_create(
        title=data_line["supplier_title"],
        address=data_line["supplier_address"],
        country=data_line["supplier_country"],
        tva_intra=data_line["supplier_tva_intra"],
        siret=data_line["siret"],
        contact=data_line["supplier_contact"],
    )
    # Payment
    payment_date = guessDate(data_line["payment_date"])
    billing_date = guessDate(data_line["billing_date"])
    billing_send_date = guessDate(data_line["billing_send_date"])
    payment = Payment.objects.create(
        number=data_line["number"],
        payment_date=payment_date,
        purchase_order=data_line["purchase_order"],
        billing_date=billing_date,
        billing_send_date=billing_send_date,
    )
    # ROYALTY
    amount = data_line["amount"] if data_line["amount"] != "" else data_line["with_tax"]
    amount = (
        Decimal(amount.replace(';', ',').replace(',', '.').replace(' ', '').replace('“', '').replace('”', ''))
        if amount
        else 0
    )
    artist_rate = data_line["artist_rate"].replace("%", '') if data_line["artist_rate"] else None
    validation_date = guessDate(data_line["validation_date"])
    royalty, created = Royalty.objects.get_or_create(
        activity=data_line["activity"],
        amount=amount,
        with_tax=data_line["with_tax"] != "",
        diffusion=diffusion,
        artist_rate=artist_rate,
        supplier=supplier,
        payment=payment,
        validation_date=validation_date,
        remark=data_line["remark"],
        money=Money(amount, 'EUR'),
    )


# Mapping entre les colonnes CSV et les champs du modèle
FIELD_MAPPING = {
    '\ufeffMONTANT HT': 'amount',
    'MONTANT TTC': 'with_tax',
    'ARTISTE RATE': 'artist_rate',
    'ITERIO': 'supplier_title',
    'PAYS': 'supplier_country',
    'TVA intra': 'supplier_tva_intra',
    'ADRESSE': 'supplier_address',
    'ACTIVITE': 'activity',
    'PERIODE': 'diff_start',
    'ARTISTE': 'name',
    'ŒUVRE': 'artwork_title',
    'DEMANDE Date': 'validation_date',
    'DEMANDE N°': 'number',
    'Facturation Date': 'billing_date',
    'Envoi Facture': 'billing_send_date',
    'PAIEMENT Date': 'payment_date',
    'REMARQUES': 'remark',
    'MAIL': 'supplier_contact',
    'CHORUS SIRET': 'siret',
    'CHORUS BON DE COMMANDE': 'purchase_order',
}


def map_csv_to_model(row):
    """Map les données d'une ligne CSV aux champs du modèle."""

    mapped_data = {}
    for csv_column, model_field in FIELD_MAPPING.items():
        mapped_data[model_field] = row.get(csv_column).strip()
    return mapped_data


def run(*args):
    # settup args
    global DRY_RUN
    if 'dry_run' in args:
        DRY_RUN = True
        print("DRY_RUN Script")
    # get the file
    fichier_csv = 'scripts/2024 - diffusion des oeuvres - royalties.csv'  #
    with open(fichier_csv, 'r') as csvfile:
        lecteur_csv = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        for row in lecteur_csv:
            data = map_csv_to_model(row)
            populateDB(data)
            # return
