from django.urls import path

from . import views

urlpatterns = [
    path("", views.TaskListView.as_view(), name="task-list"),
    path("tasks/new/", views.TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/edit/", views.TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", views.TaskDeleteView.as_view(), name="task-delete"),
    path("health/", views.health, name="health"),
]
