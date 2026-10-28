from rest_framework.routers import DefaultRouter

from .api_views import TaskViewSet


class OptionalSlashRouter(DefaultRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trailing_slash = "/?"


router = OptionalSlashRouter()
router.register("tasks", TaskViewSet, basename="task")

urlpatterns = router.urls