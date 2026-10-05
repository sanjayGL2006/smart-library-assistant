from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from core.models import Author, Book, Category, Student


class Command(BaseCommand):
    help = "Create demo admin, student and sample books"

    def handle(self, *a, **kw):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "Test@123")
        if not User.objects.filter(username="john12345").exists():
            u = User.objects.create_user("john12345", "john@example.com", "Test@123", first_name="John", last_name="Doe")
            Student.objects.create(user=u, phone="9999999999")
        c, _ = Category.objects.get_or_create(name="Programming")
        au, _ = Author.objects.get_or_create(name="Guido van Rossum")
        Book.objects.get_or_create(isbn="9780000000001", defaults=dict(name="Learning Python", category=c, author=au, price=499))
        self.stdout.write("Seeded. admin / Test@123, john12345 / Test@123")
