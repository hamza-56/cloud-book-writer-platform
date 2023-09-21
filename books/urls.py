from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path("", login_required(views.HomeView.as_view()), name="books_home"),
    path("books/add/", login_required(views.AddBookView.as_view()), name="add_book"),
    path(
        "books/<int:book_id>/",
        login_required(views.BookEditView.as_view()),
        name="book_edit",
    ),
    path(
        "books/<int:book_id>/manage_collaborators/",
        login_required(views.ManageCollaboratorsView.as_view()),
        name="manage_collaborators",
    ),
    path(
        "books/<int:book_id>/add_collaborator/",
        login_required(views.AddCollaboratorView.as_view()),
        name="add_collaborator",
    ),
    path(
        "books/<int:book_id>/remove_collaborator/<int:collaborator_id>/",
        login_required(views.RemoveCollaboratorView.as_view()),
        name="remove_collaborator",
    ),
]
