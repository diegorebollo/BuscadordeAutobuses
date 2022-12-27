from django.core.management.base import BaseCommand
from buscadorhorarios.models import Ruta
from buscadorhorarios.utils.scraper import scraper
import time


class Command(BaseCommand):
    help = "Auto Re-Scarper for rutas"

    def handle(self, *args, **kwargs):
        all_rutas = Ruta.objects.all()
        for ruta in all_rutas:
            origen = ruta.estacion_origen
            destino = ruta.estacion_destino
            ruta.delete()
            scraper_return = scraper(origen, destino)
            print(scraper_return)
            time.sleep(2)

        print('Done!')
