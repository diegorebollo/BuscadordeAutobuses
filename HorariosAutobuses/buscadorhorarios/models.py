from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from .utils.cleaning_days import cleaning_days
import json


# Create your models here.


class Estacion(models.Model):
    estacion = models.CharField(max_length=50)
    estacion_id = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = 'Estaciones'

    def __str__(self):
        return self.estacion

    def save(self, *args, **kwargs):
        # Formatting Text
        if '.' in self.estacion:
            estacion_text = self.estacion.split('.')
            self.estacion = estacion_text[0].title()
            for text in estacion_text[1:]:
                self.estacion = f'{self.estacion}.{text}'
        elif '(' in self.estacion:
            estacion_text = self.estacion.split('(')
            self.estacion = f'{estacion_text[0].title()}({estacion_text[1]}'
        else:
            self.estacion = self.estacion.title()
        super().save(*args, **kwargs)


class Ruta(models.Model):
    estacion_origen = models.ForeignKey(
        Estacion, on_delete=models.CASCADE, related_name='estacion_origen')
    estacion_destino = models.ForeignKey(
        Estacion, on_delete=models.CASCADE, related_name='estacion_destino')
    ruta_valida = models.BooleanField(default=False)
    raw_json_data = models.JSONField(null=True, blank=True)
    raw_json_periodicidad = models.JSONField(null=True, blank=True)
    slug = models.SlugField(
        verbose_name='slug (autopopulate on save)', unique=True, allow_unicode=True)
    slug_vuelta = models.SlugField(
        verbose_name='slug ruta de vuelta (autopopulate on save)', unique=True, allow_unicode=True, default=None)
    num_rutas = models.PositiveIntegerField(
        verbose_name='Numero de Rutas del Trayecto (autopopulate on save)', null=True, blank=True)
    salidas = models.JSONField(
        verbose_name='Salidas (autopopulate on save)', null=True, blank=True)
    llegadas = models.JSONField(
        verbose_name='Llegadas (autopopulate on save)', null=True, blank=True)
    servicio = models.JSONField(
        verbose_name='Servicio (autopopulate on save)', null=True, blank=True)
    fecha_ruta = models.JSONField(
        verbose_name='Fecha de la ruta (autopopulate on save)', null=True, blank=True)
    periodicidad = models.JSONField(
        verbose_name='Periodicidad (autopopulate on save)', null=True, blank=True)
    kms = models.JSONField(
        verbose_name='Kms (autopopulate on save)', null=True, blank=True)
    empresa = models.JSONField(
        verbose_name='Empresa (autopopulate on save)', null=True, blank=True)
    notas = models.JSONField(
        verbose_name='Notas (autopopulate on save)', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Rutas'

    def nombre_ruta(self):
        return f'{self.estacion_origen.estacion} - {self.estacion_destino.estacion}'

    def nombre_ruta_vuelta(self):
        return f'{self.estacion_destino.estacion} - {self.estacion_origen.estacion}'

    def __str__(self):
        return self.nombre_ruta()

    # def get_absolute_url(self):
    #     return reverse('ruta-detail-page', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre_ruta(), allow_unicode=True)
        self.slug_vuelta = slugify(
            self.nombre_ruta_vuelta(), allow_unicode=True)

        if self.ruta_valida:

            self.raw_json_data = json.loads(self.raw_json_data)

            salidas_cleaned = []
            llegadas_cleaned = []
            servicio_cleaned = []
            fecha_ruta_cleaned = []
            kms_cleaned = []
            empresa_cleaned = []
            notas_cleaned = []

            for trayecto in self.raw_json_data:
                for k, v in trayecto.items():
                    if k == 'Salida':
                        salidas_cleaned.append(v.split(' ')[0])
                        self.salidas = json.dumps(salidas_cleaned)
                    elif k == 'Llegada':
                        llegadas_cleaned.append(v.split(' ')[0])
                        self.llegadas = json.dumps(llegadas_cleaned)
                    elif k == 'Servicio':
                        servicio_cleaned.append(v)
                        self.servicio = json.dumps(servicio_cleaned)
                    elif k == 'Kms':
                        kms_cleaned.append(v)
                        self.kms = json.dumps(kms_cleaned)
                    elif k == 'Empresa':
                        empresa_cleaned.append(v)
                        self.empresa = json.dumps(empresa_cleaned)
                    elif k == 'Periodicidad':
                        split_data = v.split('.LMXJVSD')
                        split_data = list(filter(None, split_data))
                        fecha_ruta_cleaned.append(split_data)
                        self.fecha_ruta = json.dumps(fecha_ruta_cleaned)
                    elif k == 'Notas':
                        if v != None:
                            notas_cleaned.append(v.capitalize())
                        else:
                            notas_cleaned.append(str(v))
                        self.notas = json.dumps(notas_cleaned)

            self.periodicidad = cleaning_days(
                json.loads(self.raw_json_periodicidad))

            self.num_rutas = len(salidas_cleaned)

        super().save(*args, **kwargs)
