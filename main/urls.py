from django.urls import path
from . import views

urlpatterns = [

    # MAIN
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),

    # AUTH
    path("login/", views.login_view, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_view, name="logout"),

    # DASHBOARD
    path("dashboard/", views.dashboard, name="dashboard"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("admin-dashboard/site-settings/", views.site_settings, name="site_settings"),

    # STUDENTS
    path("students/add/", views.add_student, name="add_student"),
    path("students/<int:pk>/", views.view_student, name="view_student"),
    path("students/edit/<int:pk>/", views.edit_student, name="edit_student"),
    path("students/delete/<int:pk>/", views.delete_student, name="delete_student"),

    # GALLERY
    path("gallery/", views.gallery, name="gallery"),
    path("gallery/upload/", views.upload_image, name="upload_image"),
    path("gallery/edit/<int:pk>/", views.edit_image, name="edit_image"),
    path("gallery/delete/<int:pk>/", views.delete_image, name="delete_image"),

    # RESULTS
    path("results/", views.results, name="results"),

    # PROFILE
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
