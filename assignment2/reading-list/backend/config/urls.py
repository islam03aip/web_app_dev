from django.urls import include, path

urlpatterns = [
    path("api/", include("books.api_urls")),
    path("", include("books.urls")),
]
