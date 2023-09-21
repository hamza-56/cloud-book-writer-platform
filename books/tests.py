from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Book, Section


class TestBookViews(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        # Create a test book
        self.book = Book.objects.create(title="Test Book", author=self.user)

        # Create a section for the test book
        self.section = Section.objects.create(
            title="Test Section", text="Section Text", order=1, book=self.book
        )

    def test_home_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("books_home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Book")

    def test_add_book_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("add_book"),
            {
                "book-title": "New Book",
                "section-count": 1,
                "section[0]-title": "New Section",
                "section[0]-text": "New Section Text",
                "section[0]-order": 1,
            },
        )
        self.assertEqual(
            response.status_code, 302
        )  # Should redirect after creating a book
        self.assertTrue(Book.objects.filter(title="New Book").exists())

    def test_book_edit_view(self):
        response = self.client.get(reverse("book_edit", args=[self.book.id]))
        # Expect a redirection (status code 302) to the login page because login is required
        self.assertEqual(response.status_code, 302)
        # Check if the redirection URL is the login page
        self.assertRedirects(
            response,
            reverse("login") + "?next=" + reverse("book_edit", args=[self.book.id]),
        )

    def test_manage_collaborators_view(self):
        response = self.client.get(reverse("manage_collaborators", args=[self.book.id]))
        # Expect a redirection (status code 302) to the login page because login is required
        self.assertEqual(response.status_code, 302)
        # Check if the redirection URL is the login page
        self.assertRedirects(
            response,
            reverse("login")
            + "?next="
            + reverse("manage_collaborators", args=[self.book.id]),
        )

    def test_book_edit_view_logged_in(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("book_edit", args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Book")

    def test_manage_collaborators_view_logged_in(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("manage_collaborators", args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Book")

    def test_add_collaborator_view(self):
        # Create another test user
        collaborator = User.objects.create_user(
            username="collaborator", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("add_collaborator", args=[self.book.id]),
            {
                "collaborator_username": "collaborator",
            },
        )
        self.assertEqual(response.status_code, 200)  # Should return to the same page
        self.assertTrue(
            self.book.collaborators.filter(username="collaborator").exists()
        )

    def test_remove_collaborator_view(self):
        # Create another test user as a collaborator
        collaborator = User.objects.create_user(
            username="collaborator", password="testpassword"
        )
        self.book.collaborators.add(collaborator)

        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("remove_collaborator", args=[self.book.id, collaborator.id])
        )
        self.assertEqual(response.status_code, 200)  # Should return to the same page
        self.assertFalse(
            self.book.collaborators.filter(username="collaborator").exists()
        )
