from functools import wraps
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.views.decorators.http import require_POST

from .forms import CompanyForm, ContactForm, GalleryImageForm, HeroForm, ProfileForm, StudentForm
from .models import Company, Hero, Service, GalleryImage, Student, StudentResult, Profile


def get_or_create_profile(user):
    profile, _ = Profile.objects.get_or_create(
        user=user,
        defaults={"role": "admin" if (user.is_staff or user.is_superuser) else "user"},
    )

    expected_role = "admin" if (user.is_staff or user.is_superuser) else profile.role
    if (user.is_staff or user.is_superuser) and profile.role != "admin":
        profile.role = expected_role
        profile.save(update_fields=["role"])

    return profile


def admin_only(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect("login")

        if request.user.is_superuser or request.user.is_staff:
            get_or_create_profile(request.user)
            return view_func(request, *args, **kwargs)

        profile = get_or_create_profile(request.user)
        if profile.role.lower() != "admin":
            return redirect("dashboard")

        return view_func(request, *args, **kwargs)

    return wrapper


def home(request):
    home_gallery = GalleryImage.objects.filter(show_on_home=True).order_by("-uploaded_at")[:6]
    return render(request, "home.html", {
        "company": Company.objects.first(),
        "hero": Hero.objects.first(),
        "services": Service.objects.all(),
        "gallery": GalleryImage.objects.order_by('-uploaded_at')[:6],
        "home_gallery": home_gallery,
        "students": StudentResult.objects.order_by('-year')[:3],
    })


def about(request):
    return render(request, "about.html")


# ✅ REGISTER FIX
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"error": "Username already exists"})

        user = User.objects.create_user(username=username, email=email, password=password)

        # ✅ FIX
        get_or_create_profile(user)

        auth_login(request, user)
        return redirect("dashboard")

    return render(request, "register.html")


# ✅ LOGIN FIX
def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )

        # ✅ FIX
        if user is not None:
            auth_login(request, user)

            profile = get_or_create_profile(user)

            if user.is_superuser or user.is_staff or profile.role.lower() == "admin":
                return redirect("admin_dashboard")

            return redirect("dashboard")

        return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")


@login_required
@require_POST
def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def dashboard(request):
    profile = get_or_create_profile(request.user)
    return render(request, "dashboard.html", {
        "users": User.objects.count(),
        "images": GalleryImage.objects.count(),
        "students": Student.objects.count(),
        "is_admin": request.user.is_superuser or request.user.is_staff or profile.role.lower() == "admin",
    })


@login_required
@admin_only
def admin_dashboard(request):
    return render(request, "admin_dashboard.html", {
        "users": User.objects.count(),
        "students": Student.objects.count(),
        "images": GalleryImage.objects.count(),
        "student_records": Student.objects.order_by("name"),
    })


@login_required
@admin_only
def site_settings(request):
    company = Company.objects.first()
    if company is None:
        company = Company.objects.create(
            name="Ideal Techno",
            tagline="Ideas that turn into outcomes",
        )

    hero = Hero.objects.first()
    if hero is None:
        hero = Hero.objects.create(
            title="Learn with clarity, grow with confidence.",
            subtitle="Committed to your career with strong mentoring, practical learning, and the confidence to aim higher.",
            button_text="Start Your Journey",
            image_caption="Describe the hero image and what students should notice here.",
        )

    company_form = CompanyForm(request.POST or None, request.FILES or None, instance=company)
    hero_form = HeroForm(request.POST or None, request.FILES or None, instance=hero)

    if request.method == "POST" and company_form.is_valid() and hero_form.is_valid():
        company_form.save()
        hero_form.save()
        return render(
            request,
            "site_settings.html",
            {"company_form": company_form, "hero_form": hero_form, "success": True},
        )

    return render(
        request,
        "site_settings.html",
        {"company_form": company_form, "hero_form": hero_form},
    )


def gallery(request):
    is_admin = False

    if request.user.is_authenticated:
        profile = get_or_create_profile(request.user)
        if profile.role.lower() == "admin":
            is_admin = True

    return render(request, "gallery.html", {
        "images": GalleryImage.objects.all(),
        "is_admin": is_admin
    })


def results(request):
    return render(request, "results.html", {
        "students": StudentResult.objects.all()
    })


def contact(request):
    form = ContactForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        if not settings.CONTACT_EMAIL:
            form.add_error(None, "Contact email is not configured yet.")
        else:
            try:
                EmailMessage(
                    subject=f"Message from {form.cleaned_data['name']}",
                    body=form.cleaned_data["message"],
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.CONTACT_EMAIL],
                    reply_to=[form.cleaned_data["email"]],
                ).send()

                return render(request, "contact.html", {
                    "form": ContactForm(),
                    "success": True
                })
            except Exception:
                form.add_error(None, "Message could not be sent.")

    return render(request, "contact.html", {"form": form})


@login_required
def profile(request):
    profile = get_or_create_profile(request.user)
    return render(request, "profile.html", {"profile": profile})


@login_required
def edit_profile(request):
    profile = get_or_create_profile(request.user)

    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)

    if form.is_valid():
        form.save()
        return redirect("profile")

    return render(request, "edit_profile.html", {"form": form})


# ✅ STUDENT FUNCTIONS (BACK ADDED)
@login_required
@admin_only
def add_student(request):
    form = StudentForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        student = form.save()
        messages.success(request, f"Student record for {student.name} saved successfully.")
        return redirect("admin_dashboard")
    if request.method == "POST" and not form.is_valid():
        messages.error(request, "Student record could not be saved. Please correct the highlighted fields.")

    return render(request, "add_student.html", {"form": form})


@login_required
@admin_only
def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, request.FILES or None, instance=student)

    if request.method == "POST" and form.is_valid():
        student = form.save()
        messages.success(request, f"Student record for {student.name} updated successfully.")
        return redirect("admin_dashboard")
    if request.method == "POST" and not form.is_valid():
        messages.error(request, "Student record could not be updated. Please correct the highlighted fields.")

    return render(request, "edit_student.html", {"student": student, "form": form})


@login_required
@admin_only
def view_student(request, pk):
    student = get_object_or_404(Student, pk=pk)

    return render(request, "view_student.html", {"student": student})


@login_required
@admin_only
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        student_name = student.name
        student.delete()
        messages.success(request, f"Student record for {student_name} deleted successfully.")
        return redirect("admin_dashboard")

    return render(request, "delete_student_confirm.html", {"student": student})
@login_required
@admin_only
def upload_image(request):
    form = GalleryImageForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("gallery")
    if request.method == "POST" and not form.is_valid():
        messages.error(request, "Image could not be uploaded. Please correct the highlighted fields.")

    return render(request, "upload_image.html", {"form": form})


@login_required
@admin_only
def edit_image(request, pk):
    image = get_object_or_404(GalleryImage, pk=pk)
    form = GalleryImageForm(request.POST or None, request.FILES or None, instance=image)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("gallery")
    if request.method == "POST" and not form.is_valid():
        messages.error(request, "Image could not be updated. Please correct the highlighted fields.")

    return render(request, "edit_image.html", {"form": form, "gallery_image": image})


@login_required
@admin_only
def delete_image(request, pk):
    image = get_object_or_404(GalleryImage, pk=pk)

    if request.method == "POST":
        image.delete()
        return redirect("gallery")

    return render(request, "delete_image_confirm.html", {"image": image})
