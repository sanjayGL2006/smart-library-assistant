from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book, Student


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email")

    def save(self, commit=True):
        user = super().save(commit)
        return Student.objects.create(user=user, phone=self.cleaned_data["phone"])


class ProfileForm(forms.ModelForm):
    phone = forms.CharField(max_length=15, required=False)
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.fields["phone"].initial = self.instance.student.phone

    def save(self, commit=True):
        user = super().save(commit)
        user.student.phone = self.cleaned_data["phone"]
        user.student.save()
        return user


class IssueForm(forms.Form):
    student_id = forms.CharField(max_length=12)
    book = forms.ModelChoiceField(queryset=Book.objects.none())

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.fields["book"].queryset = Book.objects.exclude(issuedbook__returned_at__isnull=True)

    def clean_student_id(self):
        sid = self.cleaned_data["student_id"].strip().upper()
        try:
            return Student.objects.get(student_id=sid)
        except Student.DoesNotExist:
            raise forms.ValidationError("No student with that ID.")
