from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Crear el router y registrar los viewsets
router = DefaultRouter()
router.register(r'fincas', views.FincaViewSet, basename='finca')
router.register(r'lotes', views.LoteViewSet, basename='lote')

app_name = 'fincas'

# Las URLs se generan automáticamente desde los viewsets registrados
urlpatterns = [
    path('', include(router.urls)),
]
