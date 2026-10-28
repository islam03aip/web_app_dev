from django.urls import include, path

urlpatterns = [
    path("api/", include("tasks.api_urls")),
    path("", include("tasks.urls")),
]
