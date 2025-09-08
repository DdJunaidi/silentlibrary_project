from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Avg, Count
from django.views.decorators.http import require_POST
from django.http import HttpResponse

from .forms import ProfileForm, SignUpForm, UserUpdateForm, BookForm, AdminUserForm, ReviewForm
from .models import Book, Review, Profile

from django.utils.http import urlencode
import csv


# Create your views here.
def home(request):
    return render(request, "index.html")

def books(request):

    # views.py (top of file, after imports)
    ALLOWED_SORTS = {
    "title": "bookTitle",
    "-title": "-bookTitle",
    "author": "bookAuthor",
    "-author": "-bookAuthor",
    "new": "-created_at",
    "old": "created_at",
}


    q = request.GET.get('q', '').strip()
    genre = request.GET.get('genre', '').strip()
    status = request.GET.get('status', '').strip()

    qs = Book.objects.all()
    if q:
        qs = qs.filter(Q(bookTitle__icontains=q) | Q(bookAuthor__icontains=q))
    if genre:
        qs = qs.filter(bookGenre=genre)
    if status:
        qs = qs.filter(is_available=(status =='Available'))

    sort = request.GET.get("sort", "title")
    order_by = ALLOWED_SORTS.get(sort, "bookTitle")
    qs = qs.order_by(order_by)

    qs = qs.annotate(
        avg_rating=Avg('reviews__rating'),
        reviews_count=Count('reviews')
    )

    context = {
        'books': qs,
        'sort': sort,
        'q': q,
        'genre': genre,
        'status': status,
        'genres': Book.GENRES,
    }

    # example inside books() where you fetch books:
    books = Book.objects.all().annotate(
    avg_rating=Avg('reviews__rating'),
    reviews_count=Count('reviews')
    )

    return render(request, "books.html", context)

def contact(request):
    return render(request, "contact.html")

def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # (optional) auto-login after registration:
            login(request, user)
            messages.success(request, "Welcome to Silent Library! Your account has been created.")
            return redirect("home")
        else:
            # TEMP debugging: print errors to your terminal
            print("REGISTER ERRORS:", form.errors.as_json())
            messages.error(request, "Please fix the errors below.")
    else:
        form = SignUpForm()
    return render(request, "register.html", {"form": form})

@login_required
def dashboard(request):
    return render(request, "account/dashboard.html")

@login_required
def profile_edit(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        pform = ProfileForm(request.POST, request.FILES, instance=getattr(request.user, 'profile', None))
        if form.is_valid() and pform.is_valid():
            form.save()
            profile = pform.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, "Profile updated successfully.")
            #PRG pattern (Post/Redirect/Get) to avoid resubmits
            return redirect("profile_edit")   
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = UserUpdateForm(instance=request.user)
        Profile.objects.get_or_create(user=request.user)  # ensure profile exists
        pform = ProfileForm(instance=request.user.profile)

    return render(request, "account/profile.html", {"form": form, "pform": pform})

# -------- Simple admin area for books (staff only) --------
# Only allow signed-in staff users (admin checkbox in Django admin)
staff_required = user_passes_test(lambda u: u.is_active and u.is_staff)


@staff_required
def admin_book_list(request):
    q = request.GET.get("q", "").strip()
    books = Book.objects.all().order_by("-created_at")
    if q:
        books = books.filter(bookTitle__icontains=q)  # simple title-only search

    total = books.count()  # <-- always define total, after any filtering
    return render(
        request,
        "admin_area/book_list.html",
        {"books": books, "q": q, "total": total},
    )

@staff_required
def admin_book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Book created.")
            return redirect("admin_book_list")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = BookForm()
    return render(request, "admin_area/book_form.html", {"form": form, "mode": "create"})


@staff_required
def admin_book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Book updated.")
            return redirect("admin_book_list")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = BookForm(instance=book)
    return render(request, "admin_area/book_form.html", {"form": form, "mode": "update", "book": book})


@staff_required
def admin_book_delete(request, pk):
    """Delete via POST only (the template uses a small POST form)."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        messages.success(request, "Book deleted.")
    else:
        messages.error(request, "Deleting requires POST.")
    return redirect("admin_book_list")

@staff_required
def admin_dashboard(request):
    return render(request, "admin_area/dashboard.html")

@staff_required
def admin_user_list(request):
    q = request.GET.get("q", "").strip()
    users = User.objects.all().order_by("-date_joined")
    if q:
        users = users.filter(
            Q(username__icontains=q) |
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(email__icontains=q)
        )
    return render(request, "admin_area/users_list.html", {"users": users, "q": q})

@staff_required
def admin_user_update(request, pk):
    target = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = AdminUserForm(request.POST, instance=target)
        if form.is_valid():
            form.save()
            messages.success(request, f"Updated user “{target.username}”.")
            return redirect("admin_user_list")
        messages.error(request, "Please fix the errors below.")
    else:
        form = AdminUserForm(instance=target)
    return render(request, "admin_area/user_form.html", {"form": form, "target": target})

def book_detail(request, pk):
    book = get_object_or_404(
        Book.objects.all().annotate(
            avg_rating=Avg('reviews__rating'),
            reviews_count=Count('reviews')
        ),
        pk=pk
    )
    reviews = book.reviews.select_related('user').all()
    review_form = ReviewForm()
    return render(request, "book_detail.html", {
        "book": book,
        "reviews": reviews,
        "review_form": review_form
    })

@login_required
@require_POST
def add_review(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = ReviewForm(request.POST)
    if form.is_valid():
        # one review per (book,user) — update if exists
        Review.objects.update_or_create(
            book=book, user=request.user,
            defaults={
                "rating": form.cleaned_data["rating"],
                "comment": form.cleaned_data.get("comment", "")
            }
        )
        messages.success(request, "Thanks for your review!")
    else:
        messages.error(request, "Please correct the review form.")
    return redirect("book_detail", pk=book.pk)


@staff_required
def admin_export_books_csv(request):
    # Query with aggregates (safe on MySQL)
    qs = (Book.objects
          .annotate(avg_rating=Avg('reviews__rating'),
                    reviews_count=Count('reviews'))
          .order_by('bookTitle'))

    # Build CSV response
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="books_export.csv"'
    writer = csv.writer(response)
    writer.writerow(["Title", "Author", "Genre", "Available", "Avg Rating", "Reviews"])
    for b in qs:
        writer.writerow([
            b.bookTitle,
            b.bookAuthor,
            b.get_bookGenre_display(),
            "Yes" if b.is_available else "No",
            f"{(b.avg_rating or 0):.1f}",
            b.reviews_count or 0
        ])
    return response




    # from django.contrib import messages
# from django.contrib.auth import login
# from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required, user_passes_test
# # from django.contrib.auth.forms import UserCreationForm
# from django.shortcuts import render, redirect, get_object_or_404
# from django.db.models import Q, Avg, Count, Book

# from .forms import ProfileForm, SignUpForm, UserUpdateForm, BookForm, AdminUserForm, ReviewForm
# from .models import Book, Review, Profile
# from django.views.decorators.http import require_POST
# # from django.http import HttpResponse

# from django.db import models
# from django.http import HttpResponse

