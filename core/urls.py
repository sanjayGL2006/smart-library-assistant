from django.contrib.auth import views as auth
from django.urls import path, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from . import views as v
from .models import Author, Book, Category

F = {"template_name": "form.html"}
urlpatterns = [
    path("", v.home, name="home"),
    path("register/", v.register, name="register"),
    path("login/", csrf_exempt(auth.LoginView.as_view(template_name="form.html", extra_context={"title": "Login", "login": True})), name="login"),
    path("logout/", auth.LogoutView.as_view(next_page="home"), name="logout"),
    path("password/change/", auth.PasswordChangeView.as_view(template_name="form.html", extra_context={"title": "Change Password"}, success_url=reverse_lazy("dashboard")), name="password_change"),
    path("password/reset/", auth.PasswordResetView.as_view(), name="password_reset"),
    path("password/reset/done/", auth.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("password/reset/<uidb64>/<token>/", auth.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password/reset/complete/", auth.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path("dashboard/", v.dashboard, name="dashboard"),
    path("profile/", v.profile, name="profile"),
    path("my-books/", v.my_books, name="my_books"),
    path("books/", v.books, name="books"),
    path("notes/", v.notes_list, name="notes_list"),
    path("notes/download/<path:filename>/", v.download_note, name="download_note"),
    path("manage/issue/", v.issue_book, name="issue_book"),
    path("manage/issued/", v.issued_list, name="issued_list"),
    path("manage/return/<int:pk>/", v.return_book, name="return_book"),
    path("manage/students/", v.students, name="students"),
    path("manage/students/<int:pk>/", v.student_detail, name="student_detail"),
    path("api/students/", v.api_students, name="api_students"),
]
for model, slug, fields in [(Category, "category", ["name"]), (Author, "author", ["name"]),
                            (Book, "book", ["name", "category", "author", "isbn", "price", "note"])]:
    L, C, U, D = v.make_crud(model, slug, fields)
    urlpatterns += [path(f"manage/{slug}/", L.as_view(), name=f"{slug}_list"),
                    path(f"manage/{slug}/add/", C.as_view(), name=f"{slug}_add"),
                    path(f"manage/{slug}/<int:pk>/edit/", U.as_view(), name=f"{slug}_edit"),
                    path(f"manage/{slug}/<int:pk>/delete/", D.as_view(), name=f"{slug}_delete")]
