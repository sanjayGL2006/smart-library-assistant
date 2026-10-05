from datetime import date, timedelta
from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    class Meta: verbose_name_plural = "categories"
    def __str__(self): return self.name


class Author(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self): return self.name


class Book(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    isbn = models.CharField("ISBN", max_length=20, unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    note = models.FileField(upload_to="notes/", blank=True, null=True)

    @property
    def available(self):
        return not self.issuedbook_set.filter(returned_at__isnull=True).exists()

    def __str__(self): return f"{self.name} - {self.author} ({self.category})"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=12, unique=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.student_id:  # auto-generated on registration
            self.student_id = f"SID{1000 + self.pk}"
            super().save(update_fields=["student_id"])

    @property
    def name(self): return self.user.get_full_name() or self.user.username
    def __str__(self): return f"{self.student_id} - {self.name}"


def default_due(): return date.today() + timedelta(days=14)


class IssuedBook(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    issued_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(default=default_due)
    returned_at = models.DateTimeField(null=True, blank=True)
    class Meta: ordering = ["-issued_at"]
