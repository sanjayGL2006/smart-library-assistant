from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import IssueForm, ProfileForm, RegisterForm
from .models import Author, Book, Category, IssuedBook, Student

staff_required = user_passes_test(lambda u: u.is_staff, login_url="login")


def home(request):
    return render(request, "home.html")


def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        student = form.save()
        messages.success(request, f"Registered! Your student ID is {student.student_id}. Please log in.")
        return redirect("login")
    return render(request, "form.html", {"form": form, "title": "Student Signup"})


@login_required
def dashboard(request):
    ctx = {}
    if request.user.is_staff:
        ctx = {"books": Book.objects.count(), "authors": Author.objects.count(),
               "categories": Category.objects.count(), "students": Student.objects.count(),
               "issued": IssuedBook.objects.filter(returned_at__isnull=True).count(),
               "returned": IssuedBook.objects.filter(returned_at__isnull=False).count()}
    elif hasattr(request.user, "student"):
        rows = request.user.student.issuedbook_set
        ctx = {"student": request.user.student, "issued": rows.filter(returned_at__isnull=True).count(),
               "total": rows.count()}
    return render(request, "dashboard.html", ctx)


@login_required
def profile(request):
    if not hasattr(request.user, "student"):
        return redirect("dashboard")
    form = ProfileForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, "Profile updated.")
        return redirect("profile")
    return render(request, "form.html", {"form": form, "title": "My Profile"})


@login_required
def my_books(request):
    student = get_object_or_404(Student, user=request.user)
    return render(request, "issued.html", {"rows": student.issuedbook_set.select_related("book"), "title": "My Issued Books", "show_student": False})


@login_required
def books(request):
    return render(request, "books.html", {"books": Book.objects.select_related("author", "category")})

import os
from django.http import FileResponse, Http404

NOTES_DIR = r"C:\Users\Sanjay G L\Downloads\library\all notes"

@login_required
def notes_list(request):
    files = []
    if os.path.exists(NOTES_DIR):
        for root, _, filenames in os.walk(NOTES_DIR):
            for f in filenames:
                rel_dir = os.path.relpath(root, NOTES_DIR)
                if rel_dir == '.':
                    files.append(f)
                else:
                    files.append(os.path.join(rel_dir, f).replace('\\', '/'))
    return render(request, "notes.html", {"files": sorted(files), "total_notes": len(files)})

@login_required
def download_note(request, filename):
    safe_path = os.path.abspath(os.path.join(NOTES_DIR, filename))
    if not safe_path.startswith(os.path.abspath(NOTES_DIR)) or not os.path.exists(safe_path):
        raise Http404("File not found")
    return FileResponse(open(safe_path, 'rb'), as_attachment=False)


# ---------- Admin: category / author / book CRUD ----------
class StaffMixin(UserPassesTestMixin):
    login_url = "login"
    def test_func(self): return self.request.user.is_staff


def make_crud(model, slug, fields):
    url = reverse_lazy(f"{slug}_list")
    ctx = lambda self, c: {**c, "slug": slug, "title": model._meta.verbose_name_plural.title()}

    class L(StaffMixin, ListView):
        template_name = "list.html"
        model = None
        def get_context_data(self, **kw): return ctx(self, super().get_context_data(**kw))
    L.model = model

    class C(StaffMixin, CreateView):
        template_name = "form.html"; success_url = url
        def get_context_data(self, **kw): return {**super().get_context_data(**kw), "title": f"Add {model.__name__}"}
    C.model, C.fields = model, fields

    class U(StaffMixin, UpdateView):
        template_name = "form.html"; success_url = url
        def get_context_data(self, **kw): return {**super().get_context_data(**kw), "title": f"Edit {model.__name__}"}
    U.model, U.fields = model, fields

    class D(StaffMixin, DeleteView):
        template_name = "confirm_delete.html"; success_url = url
    D.model = model
    return L, C, U, D


# ---------- Admin: issue / return / students ----------
@staff_required
def issue_book(request):
    form = IssueForm(request.POST or None)
    if form.is_valid():
        IssuedBook.objects.create(student=form.cleaned_data["student_id"], book=form.cleaned_data["book"])
        messages.success(request, "Book issued.")
        return redirect("issued_list")
    return render(request, "form.html", {"form": form, "title": "Issue a Book"})


@staff_required
def issued_list(request):
    return render(request, "issued.html", {"rows": IssuedBook.objects.select_related("book", "student__user"), "title": "All Issued Books", "show_student": True})


@staff_required
@require_POST
def return_book(request, pk):
    row = get_object_or_404(IssuedBook, pk=pk, returned_at__isnull=True)
    row.returned_at = timezone.now()
    row.save()
    messages.success(request, "Book marked as returned.")
    return redirect("issued_list")


@staff_required
def students(request):
    return render(request, "students.html")


@staff_required
def student_detail(request, pk):
    s = get_object_or_404(Student, pk=pk)
    return render(request, "issued.html", {"rows": s.issuedbook_set.select_related("book"), "title": f"{s.name} ({s.student_id}) - {s.user.email}, {s.phone}", "show_student": False})


@staff_required
def api_students(request):
    q = request.GET.get("q", "").strip()
    qs = Student.objects.select_related("user")
    if q:
        qs = qs.filter(Q(student_id__icontains=q) | Q(user__first_name__icontains=q) | Q(user__last_name__icontains=q))
    data = [{"id": s.pk, "student_id": s.student_id, "name": s.name, "email": s.user.email,
             "phone": s.phone, "url": reverse("student_detail", args=[s.pk])} for s in qs[:50]]
    return JsonResponse({"results": data})
