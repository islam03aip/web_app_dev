from django.shortcuts import redirect, render

from .models import Task

def task_list(request):
    tasks = Task.objects.all().order_by("-created_at")

    return render(
        request,
        "todos/task_list.html",
        {"tasks": tasks},
    )


def add_task(request):
    if request.method == "POST":
        title = request.POST.get("title")

    if title:
        Task.objects.create(title=title)
    
    return redirect("task_list")


def complete_task(request, task_id):
    if request.method == "POST":
            task = Task.objects.get(id=task_id)
            task.completed = not task.completed
            task.save()

    return redirect("task_list")


def delete_task(request, task_id):
    if request.method == "POST":
        task = Task.objects.get(id=task_id)
        task.delete()

    return redirect("task_list")