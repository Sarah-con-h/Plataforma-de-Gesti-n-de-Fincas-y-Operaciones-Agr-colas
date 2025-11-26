from django.urls import path
from .views import (
    InsumoListCreateView, InsumoDetailView,
    MovimientoListCreateView, MovimientoDetailView,
    ConsumoListCreateView, ConsumoDetailView,
    resumen_inventario
)

app_name = 'insumos'

urlpatterns = [
    path('insumos/', InsumoListCreateView.as_view()),
    path('insumos/<int:pk>/', InsumoDetailView.as_view()),

    path('movimientos/', MovimientoListCreateView.as_view()),
    path('movimientos/<int:pk>/', MovimientoDetailView.as_view()),

    path('consumos/', ConsumoListCreateView.as_view()),
    path('consumos/<int:pk>/', ConsumoDetailView.as_view()),

    path('insumos/resumen/', resumen_inventario),
]