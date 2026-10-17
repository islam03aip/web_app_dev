from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import BookForm
from .models import Book


class BookListPage(ListView):
    model = Book
    template_name = "books/book_list.html"
    context_object_name = "books"

    def get_queryset(self):
        qs = Book.objects.all()
        status = self.request.GET.get("status")
        if status in Book.Status.values:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        status = self.request.GET.get("status")
        ctx["active_status"] = status if status in Book.Status.values else ""
        ctx["statuses"] = Book.Status.choices
        ctx["total"] = Book.objects.count()
        return ctx


class BookCreatePage(CreateView):
    model = Book
    form_class = BookForm
    template_name = "books/book_form.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["heading"] = "Add a book"
        ctx["submit_label"] = "Add book"
        return ctx


class BookUpdatePage(UpdateView):
    model = Book
    form_class = BookForm
    template_name = "books/book_form.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["heading"] = "Edit book"
        ctx["submit_label"] = "Save changes"
        return ctx


class BookDeletePage(DeleteView):
    model = Book
    template_name = "books/book_confirm_delete.html"
    success_url = reverse_lazy("home")
