
import csv, datetime, urllib, argparse

import dateutil.parser
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from django.contrib.auth.models import User

from slugify import slugify
import dateutil
from decimal import Decimal
from djmoney.money import Money

from royalties.models import ( Artist, Artwork, Diffusion, Supplier, Royalty, Payment, Notification,)



def guessDate(date_str, default=None):
    if(date_str != ""):
        date_str = "01/05/2024" if date_str=="mai" else date_str
        date_str = "01/03/2024" if date_str=="mars" else date_str
        date_str = "01/02/2024" if date_str=="fevrier" or date_str=="février" else date_str
        date_str = "01/01/2024" if date_str=="janvier" else date_str
        date_str = "01/07/2024" if date_str=="S2 2023" or date_str=="S2/2023" else date_str
        multidates = ("-", "au", "+")
        for sep in multidates:
            if(sep in date_str):
                print(date_str)
                date_split = date_str.split(sep)
                if(len(date_split[0]) > 2):
                    date_str = date_split[0] 
                elif "/" in date_split[1]:
                    date_str = date_split[0] + "/" + date_split[1].split("/")[1]
                date_str+= "/2024"
        try:
            date = dateutil.parser.parse(date_str)
            print("trouvé : " + str(date))
            return date
        except Exception as e:
            print(e)
            print("Date non reconnu : " + date_str)
            new_date_str = input("Entrez une date : ")
            if( new_date_str != ""):
                return guessDate(new_date_str)
    return default


def populateDB(data_line):
    name = data_line["name"].title()
    artist, created = Artist.objects.get_or_create(name=name)
    # if(created):
    #     artist.contact = 
    artwork, created = Artwork.objects.get_or_create(title=data_line["artwork_title"], artist=artist)
    # DIFF
    diff_date_start = guessDate(data_line["diff_start"], datetime.datetime.now())
    diffusion, created = Diffusion.objects.get_or_create(title=data_line["supplier_title"], start=diff_date_start, artist=artist, artwork=artwork)
    # SUPPLIER
    supplier, created = Supplier.objects.get_or_create(title=data_line["supplier_title"],
                                                       address=data_line["supplier_address"],
                                                       country=data_line["supplier_country"],
                                                       tva_intra=data_line["supplier_tva_intra"],
                                                       siret=data_line["siret"],
                                                       contact=data_line["supplier_contact"],)
    # Payment
    payment_date=guessDate(data_line["payment_date"])
    billing_date = guessDate(data_line["billing_date"])
    billing_send_date = guessDate(data_line["billing_send_date"])
    payment = Payment.objects.create(number=data_line["number"],
                                                payment_date=payment_date,
                                                purchase_order=data_line["purchase_order"],
                                                billing_date=billing_date,
                                                billing_send_date=billing_send_date,)
    # ROYALTY
    amount = data_line["amount"] if data_line["amount"]!="" else data_line["with_tax"]
    amount = Decimal(amount.replace(';',',').replace(',','.').replace(' ','').replace('“','').replace('”','')) if amount else 0
    artist_rate = data_line["artist_rate"].replace("%",'') if data_line["artist_rate"] else None
    validation_date = guessDate(data_line["validation_date"])
    royalty, created = Royalty.objects.get_or_create(activity=data_line["activity"], 
                                    amount=amount,
                                    with_tax=data_line["with_tax"]!="",
                                    diffusion=diffusion,
                                    artist_rate=artist_rate,
                                    supplier=supplier,
                                    payment=payment,
                                    validation_date=validation_date,                                    
                                    remark=data_line["remark"],
                                    money=Money(amount,'EUR')
                                    )

    



# Mapping entre les colonnes CSV et les champs du modèle
FIELD_MAPPING = {
    '\ufeffMONTANT HT':'amount',
    'MONTANT TTC':'with_tax',
    'ARTISTE RATE':'artist_rate',
    'ITERIO':'supplier_title',
    'PAYS':'supplier_country',
    'TVA intra':'supplier_tva_intra',
    'ADRESSE':'supplier_address',
    'ACTIVITE':'activity',
    'PERIODE':'diff_start',
    'ARTISTE':'name',
    'ŒUVRE':'artwork_title',
    'DEMANDE Date':'validation_date',
    'DEMANDE N°':'number',
    'Facturation Date':'billing_date',
    'Envoi Facture':'billing_send_date',
    'PAIEMENT Date':'payment_date',
    'REMARQUES':'remark',
    'MAIL':'supplier_contact',
    'CHORUS SIRET':'siret',
    'CHORUS BON DE COMMANDE':'purchase_order',
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
        lecteur_csv = csv.DictReader(csvfile, delimiter=';', quotechar='"' )
        for row in lecteur_csv:
            data = map_csv_to_model(row)
            populateDB(data)
            # return