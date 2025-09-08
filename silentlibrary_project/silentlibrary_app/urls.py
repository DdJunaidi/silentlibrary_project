from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    #public pages
    path("", views.home, name="home"),
    path("books/", views.books, name="books"),
    path("books/<int:pk>/", views.book_detail, name="book_detail"),
    path("books/<int:pk>/review/", views.add_review, name="add_review"),
    path("contact/", views.contact, name="contact"),

    #register new user
    path("register/", views.register, name="register"),

    # auth
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html",
            redirect_authenticated_user=True
        ),
        name="login",
    ),
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),

    # personalized pages
    path("me/", views.dashboard, name="dashboard"),
    path("me/profile/", views.profile_edit, name="profile_edit"),

    #admin area for books (staff only)
    path("min/books/", views.admin_book_list, name="admin_book_list"),
    path("min/books/new/", views.admin_book_create, name="admin_book_create"),
    path("min/books/<int:pk>/edit/", views.admin_book_update, name="admin_book_update"),
    path("min/books/<int:pk>/delete/", views.admin_book_delete, name="admin_book_delete"),
    path("min/", views.admin_dashboard, name="admin_dashboard"),
    path("min/users/", views.admin_user_list, name="admin_user_list"),
    path("min/users/<int:pk>/", views.admin_user_update, name="admin_user_update"),
    path("min/books/export/", views.admin_export_books_csv, name="admin_export_books_csv"),
 

]


    #password reset
    # path("reset_password/", 
    #      auth_views.PasswordResetView.as_view(
    #          template_name='registration/password_reset_form.html',
    #          email_template_name='registration/reset_password_email.html',
    #          subject_template_name='registration/reset_password_subject.txt',
    #          success_url='/reset_password/done/'
    #      ),
    #      name="reset_password"),
    # path("reset_password/done/",
    #      auth_views.PasswordResetDoneView.as_view(
    #          template_name='registration/password_reset_done.html'
    #      ),
    #      name="password_reset_done"),
    # path("reset-password/confirm/<uidb64>/<token>/",
    #      auth_views.PasswordResetConfirmView.as_view(
    #          template_name='registration/password_reset_confirmation.html',
    #          success_url='/reset-password/complete/'
    #      ),
    #      name="password_reset_confirm"),
    # path("reset-password/complete/",
    #      auth_views.PasswordResetCompleteView.as_view(
    #          template_name='registration/password_reset_complete.html'
    #      ),
    #      name="password_reset_complete"),

