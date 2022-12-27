from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.views import View
from django.db.models import Q
from .forms import BuscadorForm
from .models import Estacion, Ruta
from .utils.scraper import scraper
import json

# Create your views here.


class IndexView(FormView):
    template_name = 'buscadorhorarios/index.html'
    form_class = BuscadorForm
    model_estacion = Estacion
    model_ruta = Ruta

    def get(self, request):
        if 'term' in request.GET:
            qs = self.model_estacion.objects.filter(
                estacion__startswith=request.GET.get('term')).order_by('estacion')[:5]
            lista_estaciones = []
            for estacion in qs:
                lista_estaciones.append(estacion.estacion)
            return JsonResponse(lista_estaciones, safe=False)
        return render(request, self.template_name, {'form': self.form_class})

    def form_valid(self, form):
        try:
            user_origen = self.model_estacion.objects.get(
                Q(estacion__startswith=form.cleaned_data['origen']))
            user_destino = self.model_estacion.objects.get(
                Q(estacion__startswith=form.cleaned_data['destino']))
        except:
            return render(self.request, self.template_name, {'form': self.form_class, 'error': 'Origen o Destino no válido'})
        try:
            qs = self.model_ruta.objects.get(Q(estacion_origen__estacion_id=user_origen.estacion_id) & Q(
                estacion_destino__estacion_id=user_destino.estacion_id))
        except:
            slug = scraper(user_origen, user_destino)
            if slug == None:
                return render(self.request, self.template_name, {'form': self.form_class, 'error': 'Ruta no disponible'})
            else:
                return HttpResponseRedirect(reverse('ruta-detail-page', args=[slug]))
        else:
            if qs.ruta_valida:
                return HttpResponseRedirect(reverse('ruta-detail-page', args=[qs.slug]))
            else:
                return render(self.request, self.template_name, {'form': self.form_class, 'error': 'Ruta no disponible'})


class RutaView(DetailView):
    model = Ruta
    template_name = 'buscadorhorarios/resultado.html'
    context_object_name = 'ruta'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        qs = get_object_or_404(self.model, slug=self.kwargs.get('slug'))

        if qs.ruta_valida:
            salidas = json.loads(qs.salidas)
            llegadas = json.loads(qs.llegadas)
            servicio = json.loads(qs.servicio)
            fecha_ruta = json.loads(qs.fecha_ruta)
            kms = json.loads(qs.kms)
            empresa = json.loads(qs.empresa)
            notas = json.loads(qs.notas)
            periodicidad = json.loads(qs.periodicidad)
            context['user_origen'] = qs.estacion_origen.estacion_id
            context['user_destino'] = qs.estacion_destino.estacion_id
            context['estacion_origen'] = qs.estacion_origen.estacion.split('(')[
                0]
            context['estacion_destino'] = qs.estacion_destino.estacion.split('(')[
                0]
            context['json_trayectos'] = zip(
                salidas, llegadas, servicio, fecha_ruta, kms, empresa, notas, periodicidad)

            return context
        else:
            raise Http404('Ruta no valida')


def vuelta_view(request, origen, destino):
    model_estacion = Estacion
    model_ruta = Ruta

    try:
        user_origen = model_estacion.objects.get(
            Q(estacion_id=origen))
        user_destino = model_estacion.objects.get(
            Q(estacion_id=destino))
    except:
        raise Http404('Origen o Destino no válido')

    try:
        slug = model_ruta.objects.get(Q(estacion_origen__estacion_id=origen) & Q(
            estacion_destino__estacion_id=destino)).slug
    except:
        slug = scraper(user_origen, user_destino)
        if slug == None:
            raise Http404('Ruta no disponible')
    finally:
        return HttpResponseRedirect(reverse('ruta-detail-page', args=[slug]))
