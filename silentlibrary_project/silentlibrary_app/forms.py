from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book, Review, Profile

# registration of new user
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user

# Edit user profile
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name":  forms.TextInput(attrs={"class": "form-control"}),
            "email":      forms.EmailInput(attrs={"class": "form-control"}),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            # Prevent using an email that belongs to another user
            qs = User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("This email is already used by another account.")
        return email

# Admin form to manage Book entries    
class BookForm(forms.ModelForm):
  class Meta:
      model = Book
      fields = ["bookTitle", "bookAuthor", "bookGenre", "is_available"]
      widgets = {
          "bookTitle":  forms.TextInput(attrs={"class": "form-control"}),
          "bookAuthor": forms.TextInput(attrs={"class": "form-control"}),
          "bookGenre":  forms.Select(attrs={"class": "form-select"}),
          "cover":      forms.ClearableFileInput(attrs={"class": "form-control"}),
          "is_available": forms.CheckboxInput(attrs={"class": "form-check-input"}),
      }

class AdminUserForm(forms.ModelForm):
    # Show username but don't allow changing it here
    username = forms.CharField(
        disabled=True, required=False, label="Username",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "is_active", "is_staff"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name":  forms.TextInput(attrs={"class": "form-control"}),
            "email":      forms.EmailInput(attrs={"class": "form-control"}),
            "is_active":  forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_staff":   forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

# NEW: Profile photo form
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["photo"]
        widgets = {
            "photo": forms.ClearableFileInput(attrs={"class": "form-control"})
        }

# NEW: Review form
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.NumberInput(attrs={"class": "form-control", "min":1, "max":5}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows":3}),
        }

#   def clean_email(self):
#       email = self.cleaned_data.get("email")
#       if email:
#           qs = User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
#           if qs.exists():
#               raise forms.ValidationError("This email is already used by another account.")
#       return email
