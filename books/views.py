from django.db.models import Q
from django.views import View
from django.db import transaction
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from django.shortcuts import redirect, render, get_object_or_404

from .forms import BookForm
from .models import Book, Section

User = get_user_model()


class HomeView(TemplateView):
    template_name = "books/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Retrieve books where the user is either the author or a collaborator
        user_books = Book.objects.filter(Q(author=user) | Q(collaborators=user))
        # TODO: implement pagination
        context["user_books"] = user_books
        return context


class AddBookView(View):
    @transaction.atomic
    def post(self, request):
        book_title = request.POST.get("book-title", "")
        section_count = int(request.POST.get("section-count", "0"))
        try:
            book = Book.objects.create(title=book_title, author=request.user)

            parent_section_map = {}

            for section_idx in range(section_count):
                section_id = request.POST.get(f"section[{section_idx}]-id", "")
                section_title = request.POST.get(f"section[{section_idx}]-title", "")
                section_text = request.POST.get(f"section[{section_idx}]-text", "")
                section_order = request.POST.get(f"section[{section_idx}]-order", "")
                parent_section_id = request.POST.get(
                    f"section[{section_idx}]-parent_section", ""
                )
                # TODO: use bulk-create
                section = Section.objects.create(
                    title=section_title,
                    text=section_text,
                    order=section_order,
                    parent_section_id=parent_section_map.get(parent_section_id)
                    if parent_section_id
                    else None,
                    book=book,
                )
                parent_section_map[section_id] = section.id

            return redirect("books_home")
        except:
            messages.error(request, "Unable to create book")
            return redirect("add_book")

    def get(self, request):
        book_form = BookForm(prefix="book")
        return render(
            request,
            "books/add_book.html",
            {
                "book_form": book_form,
            },
        )


class BookDetailView(TemplateView):
    template_name = "books/book_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_id = self.kwargs.get("book_id")
        book = get_object_or_404(Book, pk=book_id)
        context["book"] = book
        return context


class ManageCollaboratorsView(TemplateView):
    template_name = "books/manage_collaborators.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_id = self.kwargs.get("book_id")
        book = get_object_or_404(Book, pk=book_id)
        context["book"] = book
        return context


class AddCollaboratorView(View):
    template_name = "books/manage_collaborators.html"

    def post(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        collaborator_username = request.POST.get("collaborator_username")

        try:
            collaborator = User.objects.get(username=collaborator_username)
            if collaborator == request.user:
                messages.error(request, "You cannot add yourself as a collaborator.")
            elif collaborator in book.collaborators.all():
                messages.error(request, "User is already a collaborator.")
            elif request.user != book.author:
                messages.error(
                    request, "You do not have permission to add collaborators."
                )
            else:
                book.collaborators.add(collaborator)

                messages.success(
                    request,
                    f"Successfully added {collaborator_username} as a collaborator.",
                )
        except User.DoesNotExist:
            messages.error(
                request,
                f"Invalid username. User {collaborator_username} doesn't exist.",
            )

        return render(request, self.template_name, {"book": book})


class RemoveCollaboratorView(View):
    template_name = "books/manage_collaborators.html"

    def post(self, request, book_id, collaborator_id):
        book = Book.objects.get(pk=book_id)
        collaborator = User.objects.get(pk=collaborator_id)

        if request.user == book.author:
            book.collaborators.remove(collaborator)
            messages.success(
                request, f"{collaborator.username} removed as a collaborator."
            )
        else:
            messages.error(
                request, "You do not have permission to remove a collaborator."
            )

        return render(request, self.template_name, {"book": book})
