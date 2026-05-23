from django.contrib import admin

from .models import Company, GalleryImage, Hero, Profile, Service, Student, StudentResult


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["name", "tagline", "primary_color", "accent_color"]
    search_fields = ["name"]


@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ["title", "button_text"]
    search_fields = ["title", "image_caption"]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["title"]
    search_fields = ["title"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "role", "school_name", "phone"]
    list_filter = ["role"]
    search_fields = ["user__username", "school_name"]


@admin.register(GalleryImage)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "show_on_home", "uploaded_at"]
    list_filter = ["category", "show_on_home"]
    search_fields = ["title", "description"]
    ordering = ["-uploaded_at"]
    actions = ["mark_as_featured", "show_selected_on_home", "hide_selected_from_home"]

    def mark_as_featured(self, request, queryset):
        queryset.update(category="featured")

    def show_selected_on_home(self, request, queryset):
        queryset.update(show_on_home=True)

    def hide_selected_from_home(self, request, queryset):
        queryset.update(show_on_home=False)

    mark_as_featured.short_description = "Mark selected as Featured"
    show_selected_on_home.short_description = "Show selected images on Home"
    hide_selected_from_home.short_description = "Hide selected images from Home"


@admin.register(StudentResult)
class StudentResultAdmin(admin.ModelAdmin):
    list_display = ["name", "exam_name", "marks", "year", "result_status"]
    list_filter = ["year"]
    search_fields = ["name", "exam_name"]

    def result_status(self, obj):
        try:
            return "Pass" if float(obj.marks) >= 40 else "Fail"
        except (TypeError, ValueError):
            return "Unknown"


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "student_no",
        "gender",
        "category",
        "email_id",
        "guardian_phone_no",
        "university_year",
    ]
    list_filter = ["gender", "category", "tenth_year", "twelfth_year", "university_year"]
    search_fields = [
        "name",
        "student_no",
        "email_id",
        "guardian_phone_no",
        "adhar_card_no",
        "ssmid_no",
    ]
    date_hierarchy = "dob"
    ordering = ["name"]
    readonly_fields = ["created_at", "updated_at"]
    list_per_page = 25
    fieldsets = (
        ("Student Details", {
            "fields": (
                "name",
                "student_no",
                "gender",
                "dob",
                "category",
                "photo",
            )
        }),
        ("Family Contact", {
            "fields": (
                "father_name_or_husband_name",
                "father_or_husband_occupation",
                "email_id",
                "guardian_phone_no",
                "permanent_address",
                "present_address",
            )
        }),
        ("Academic Record", {
            "fields": (
                "tenth_board_name",
                "tenth_marks",
                "tenth_year",
                "twelfth_board_name",
                "twelfth_marks",
                "twelfth_year",
                "university_name",
                "university_cgpa_or_percentage",
                "university_year",
            )
        }),
        ("Identity Numbers", {
            "fields": ("adhar_card_no", "ssmid_no")
        }),
        ("System Fields", {
            "fields": ("created_at", "updated_at")
        }),
    )
