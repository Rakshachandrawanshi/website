import os

from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_migrate, post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def ensure_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            Profile.objects.get_or_create(user=instance, defaults={'role': 'admin'})
        else:
            Profile.objects.get_or_create(user=instance, defaults={'role': 'user'})


@receiver(post_migrate)
def seed_public_site_content(sender, app_config, apps, **kwargs):
    if app_config.name != "main":
        return

    Company = apps.get_model("main", "Company")
    Hero = apps.get_model("main", "Hero")
    Service = apps.get_model("main", "Service")
    User = apps.get_model("auth", "User")
    Profile = apps.get_model("main", "Profile")

    Company.objects.get_or_create(
        defaults={
            "name": "Ideal Techno",
            "tagline": "Coaching for confident achievers",
            "primary_color": "#17378f",
            "accent_color": "#ffc928",
            "surface_tint": "#f4f8ff",
        }
    )

    Hero.objects.get_or_create(
        defaults={
            "title": "Dream bigger. Study smarter. Achieve with confidence.",
            "subtitle": "A modern coaching environment with expert faculty, disciplined schedules, and personal mentoring for school, entrance, and career-focused learners.",
            "button_text": "Enroll Now",
            "image_caption": "Weekly tests, doubt support, and clear feedback help students move forward with confidence.",
        }
    )

    default_services = [
        (
            "Foundation Batches",
            "Strong concepts for classes 8-10 with regular practice and parent-friendly progress updates.",
        ),
        (
            "Board Excellence",
            "Syllabus-focused preparation with writing practice, revision cycles, and confidence-building tests.",
        ),
        (
            "Entrance Prep",
            "Exam-oriented coaching for ambitious students with mock tests, analytics, and doubt clearing.",
        ),
    ]
    for title, description in default_services:
        Service.objects.get_or_create(title=title, defaults={"description": description})

    username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
    email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")
    password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

    if username and password:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "is_staff": True,
                "is_superuser": True,
            },
        )
        changed = False
        if not user.is_staff:
            user.is_staff = True
            changed = True
        if not user.is_superuser:
            user.is_superuser = True
            changed = True
        if email and user.email != email:
            user.email = email
            changed = True
        if password:
            user.password = make_password(password)
            changed = True
        if changed:
            user.save()
        Profile.objects.get_or_create(user=user, defaults={"role": "admin"})
