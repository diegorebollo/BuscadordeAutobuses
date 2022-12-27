from django.contrib import admin
from .models import Estacion, Ruta
# Register your models here.


class RutaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('estacion_origen', 'estacion_destino')}


admin.site.register(Ruta, RutaAdmin)
admin.site.register(Estacion)
