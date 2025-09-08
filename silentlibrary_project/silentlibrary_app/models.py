from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Book(models.Model):
    GENRES = [
        ("drama", "Drama"),
        ("thriller", "Thriller"),
        ("horror", "Horror"),
        ("comedy", "Comedy"),
        ("documentary", "Documentary"),
    ]
    bookID = models.AutoField(primary_key=True)
    bookTitle = models.CharField(max_length=200)
    bookAuthor = models.CharField(max_length=200)
    bookGenre = models.CharField(max_length=20, choices=GENRES, blank=True)
    cover = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bookTitle} by {self.bookAuthor}"

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    photo = models.ImageField(upload_to="profiles/", blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='book_reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('book', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.book.bookTitle} — {self.rating}★ by {self.user.username}"
    

class Publisher(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
