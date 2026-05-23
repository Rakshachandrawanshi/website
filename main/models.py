import os
import uuid

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator, validate_image_file_extension
from django.db import models
from django.utils.text import get_valid_filename


MAX_IMAGE_UPLOAD_SIZE = 10 * 1024 * 1024


def validate_image_size(image):
    if image and image.size > MAX_IMAGE_UPLOAD_SIZE:
        raise ValidationError("Image file size must be 10MB or less.")


image_validators = [validate_image_file_extension, validate_image_size]


phone_validator = RegexValidator(
    regex=r"^\+?[0-9]{10,15}$",
    message="Enter a valid phone number with 10 to 15 digits.",
)


adhar_validator = RegexValidator(
    regex=r"^[0-9]{12}$",
    message="Adhar card number must be exactly 12 digits.",
)


ssmid_validator = RegexValidator(
    regex=r"^[0-9]{8,20}$",
    message="SSMID number must contain 8 to 20 digits.",
)


def student_photo_upload_path(instance, filename):
    base, extension = os.path.splitext(filename or "")
    safe_base = get_valid_filename(base) or "student-photo"
    return f"students/photos/{safe_base}-{uuid.uuid4().hex}{extension.lower()}"


# ===============================
# COMPANY SETTINGS (CMS)
# ===============================
class Company(models.Model):
    name = models.CharField(max_length=200)
    tagline = models.TextField()
    logo = models.ImageField(upload_to="company/", blank=True, null=True, validators=image_validators)
    favicon = models.ImageField(upload_to="company/", blank=True, null=True, validators=image_validators)
    primary_color = models.CharField(max_length=7, default="#17378f")
    accent_color = models.CharField(max_length=7, default="#2850af")
    surface_tint = models.CharField(max_length=7, default="#f4f8ff")

    def __str__(self):
        return self.name


# ===============================
# HERO SECTION
# ===============================
class Hero(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.TextField()
    button_text = models.CharField(max_length=100, default="Get Started")
    image = models.ImageField(upload_to="hero/", blank=True, null=True, validators=image_validators)
    image_caption = models.TextField(blank=True)

    def __str__(self):
        return self.title


# ===============================
# SERVICES
# ===============================
class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.title


# ===============================
# GALLERY
# ===============================
class GalleryImage(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="gallery/", validators=image_validators)
    category = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    show_on_home = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ===============================
# STUDENT RESULTS
# ===============================
class StudentResult(models.Model):
    name = models.CharField(max_length=200)
    exam_name = models.CharField(max_length=200)
    rank = models.CharField(max_length=50)
    marks = models.CharField(max_length=50)
    photo = models.ImageField(upload_to="results/", validators=image_validators)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.exam_name})"


class Student(models.Model):
    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    )

    CATEGORY_CHOICES = (
        ("GEN", "GEN"),
        ("ST", "ST"),
        ("SC", "SC"),
        ("OBC", "OBC"),
    )

    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    father_name_or_husband_name = models.CharField(max_length=255)
    father_or_husband_occupation = models.CharField(max_length=255)
    email_id = models.EmailField(unique=True)
    guardian_phone_no = models.CharField(max_length=16, validators=[phone_validator])
    permanent_address = models.TextField()
    present_address = models.TextField()
    student_no = models.CharField(max_length=50, unique=True, db_index=True)
    dob = models.DateField(verbose_name="Date of Birth")
    category = models.CharField(max_length=3, choices=CATEGORY_CHOICES)
    tenth_board_name = models.CharField(max_length=255)
    tenth_marks = models.DecimalField(max_digits=5, decimal_places=2)
    tenth_year = models.PositiveIntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2100)])
    twelfth_board_name = models.CharField(max_length=255)
    twelfth_marks = models.DecimalField(max_digits=5, decimal_places=2)
    twelfth_year = models.PositiveIntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2100)])
    university_name = models.CharField(max_length=255)
    university_cgpa_or_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    university_year = models.PositiveIntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2100)])
    photo = models.ImageField(
        upload_to=student_photo_upload_path,
        validators=image_validators,
    )
    adhar_card_no = models.CharField(max_length=12, unique=True, db_index=True, validators=[adhar_validator])
    ssmid_no = models.CharField(max_length=20, unique=True, db_index=True, validators=[ssmid_validator])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["student_no"]),
            models.Index(fields=["adhar_card_no"]),
            models.Index(fields=["ssmid_no"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.student_no})"


# ===============================
# USER PROFILE (ROLE SYSTEM)
# ===============================
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    ROLE_CHOICES = (
        ("user", "User"),
        ("admin", "Admin"),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")
    school_name = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    image = models.ImageField(
        upload_to="profile_images/",
        default="profile_images/default.png",
        validators=image_validators,
    )

    def __str__(self):
        return f"{self.user.username} ({self.role})"
