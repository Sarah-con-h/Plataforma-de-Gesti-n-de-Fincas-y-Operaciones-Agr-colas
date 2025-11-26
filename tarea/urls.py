from rest_framework.routers import DefaultRouter
from .views import TipoTareaViewSet, TareaViewSet

router = DefaultRouter()
router.register('tipos-tarea', TipoTareaViewSet, basename='tipotarea')
router.register('tareas', TareaViewSet, basename='tarea')

app_name = 'tarea'
urlpatterns = router.urls
