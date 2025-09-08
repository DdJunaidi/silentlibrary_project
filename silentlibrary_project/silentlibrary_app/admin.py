from django.contrib import admin
from .models import Book, Review, Profile

#register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("bookTitle", "bookAuthor", "bookGenre", "is_available", "created_at")
    list_filter = ("bookGenre", "is_available")
    search_fields = ("bookTitle", "bookAuthor")

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("book", "user", "rating", "created_at")
    list_filter = ("rating",)
    search_fields = ("book__bookTitle", "user__username", "comment")