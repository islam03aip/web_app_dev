from rest_framework.routers import DefaultRouter

from .views import AuthorViewSet, BookViewSet, CategoryViewSet, ReviewViewSet

router = DefaultRouter()
router.register("authors", AuthorViewSet, basename="author")
router.register("books", BookViewSet, basename="book")
router.register("categories", CategoryViewSet, basename="category")
router.register("reviews", ReviewViewSet, basename="review")

urlpatterns = router.urls
