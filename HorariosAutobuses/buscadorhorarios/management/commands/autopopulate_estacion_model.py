from django.core.management.base import BaseCommand
from buscadorhorarios.models import Estacion
import json


class Command(BaseCommand):
    help = "Auto Populate Estacion's Model with JSON data"

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='JSON FILE PATH')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        with open(file_path, 'r') as f:
            file = json.load(f)

        user_input = input(
            f'{len(file)} new entries will be created in buscadorhorarios.models.Estacion from {file_path}\nDo you want to continue? (YES/NO) ')

        if user_input.lower() in ('yes', 'y'):
            for k, v in file.items():
                Estacion.objects.create(estacion=k, estacion_id=v)
            print('Done!')
