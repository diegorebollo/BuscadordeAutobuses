from django.urls import path
from .views import IndexView, RutaView, vuelta_view

urlpatterns = [
    path('', IndexView.as_view(), name='index-page'),
    path('ruta/<slug:slug>', RutaView.as_view(), name='ruta-detail-page'),
    path('vuelta/<int:origen>/<int:destino>',
         vuelta_view, name='get-vuelta')
]
