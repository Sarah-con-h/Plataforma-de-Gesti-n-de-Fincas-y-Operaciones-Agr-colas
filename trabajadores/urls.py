from rest_framework.routers import DefaultRouter
from .views import TrabajadorViewSet, AsignacionViewSet

router = DefaultRouter()
router.register(r'trabajadores', TrabajadorViewSet, basename='trabajador')
router.register(r'asignaciones', AsignacionViewSet, basename='asignacion')

urlpatterns = router.urls