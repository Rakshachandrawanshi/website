from django.contrib import admin
from django.contrib.auth.models import User
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.test.utils import override_settings
from django.urls import reverse

from .admin import StudentResultAdmin
from .forms import StudentForm
from .models import GalleryImage, Profile, Student, StudentResult


class RegistrationTests(TestCase):
    def test_register_page_submit_button_does_not_disable_before_submit(self):
        response = self.client.get(reverse("register"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="register-submit"')
        self.assertNotContains(response, 'onclick="this.disabled=true; this.innerText=\'Creating...\'"')

    def test_register_creates_single_profile_and_redirects(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "safe-password-123",
            },
        )

        self.assertRedirects(response, reverse("dashboard"))
        user = User.objects.get(username="newuser")
        self.assertEqual(Profile.objects.filter(user=user).count(), 1)

    def test_superuser_profile_is_synced_to_admin_role(self):
        admin_user = User.objects.create_superuser(
            username="boss",
            email="boss@example.com",
            password="boss-pass-123",
        )

        profile = Profile.objects.get(user=admin_user)

        self.assertEqual(profile.role, "admin")


class LoginFlowTests(TestCase):
    def test_login_page_submit_button_does_not_disable_before_submit(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="login-submit"')
        self.assertNotContains(response, 'onclick="this.disabled=true; this.innerText=\'Logging in...\'"')

    def test_login_restores_missing_profile_and_redirects_to_dashboard(self):
        user = User.objects.create_user(
            username="profileless",
            email="profileless@example.com",
            password="safe-password-123",
        )
        Profile.objects.filter(user=user).delete()

        response = self.client.post(
            reverse("login"),
            {"username": "profileless", "password": "safe-password-123"},
        )

        self.assertRedirects(response, reverse("dashboard"))
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_logout_requires_post(self):
        User.objects.create_user(
            username="logoutuser",
            email="logout@example.com",
            password="safe-password-123",
        )
        self.client.login(username="logoutuser", password="safe-password-123")

        get_response = self.client.get(reverse("logout"))
        post_response = self.client.post(reverse("logout"))

        self.assertEqual(get_response.status_code, 405)
        self.assertRedirects(post_response, reverse("home"))


class StudentManagementViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username="adminuser",
            email="admin@example.com",
            password="admin-pass-123",
        )
        self.admin_user.profile.role = "admin"
        self.admin_user.profile.save()
        self.regular_user = User.objects.create_user(
            username="regularuser",
            email="regular@example.com",
            password="user-pass-123",
        )
        self.student = Student.objects.create(
            name="Student One",
            gender="Male",
            father_name_or_husband_name="Parent One",
            father_or_husband_occupation="Teacher",
            email_id="student.one@example.com",
            guardian_phone_no="9876543210",
            permanent_address="Permanent Address",
            present_address="Present Address",
            student_no="STU-1001",
            dob="2004-01-15",
            category="GEN",
            tenth_board_name="CBSE",
            tenth_marks="89.50",
            tenth_year=2020,
            twelfth_board_name="CBSE",
            twelfth_marks="91.25",
            twelfth_year=2022,
            university_name="ABC University",
            university_cgpa_or_percentage="8.40",
            university_year=2025,
            photo=SimpleUploadedFile("student.png", MINIMAL_PNG, content_type="image/png"),
            adhar_card_no="123456789012",
            ssmid_no="12345678",
        )

    def test_delete_student_uses_existing_confirmation_template(self):
        self.client.login(username="adminuser", password="admin-pass-123")

        response = self.client.get(reverse("delete_student", args=[self.student.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "delete_student_confirm.html")

    def test_non_admin_cannot_open_student_add_page(self):
        self.client.login(username="regularuser", password="user-pass-123")

        response = self.client.get(reverse("add_student"))

        self.assertRedirects(response, reverse("dashboard"))

    def test_admin_can_create_student_record_from_form(self):
        self.client.login(username="adminuser", password="admin-pass-123")
        response = self.client.post(
            reverse("add_student"),
            {
                "name": "Aman Sharma",
                "gender": "Male",
                "father_name_or_husband_name": "Rakesh Sharma",
                "father_or_husband_occupation": "Teacher",
                "email_id": "aman@example.com",
                "guardian_phone_no": "9988776655",
                "permanent_address": "Permanent Address",
                "present_address": "Present Address",
                "student_no": "STU-2002",
                "dob": "2004-01-15",
                "category": "OBC",
                "tenth_board_name": "CBSE",
                "tenth_marks": "88.50",
                "tenth_year": 2020,
                "twelfth_board_name": "CBSE",
                "twelfth_marks": "91.25",
                "twelfth_year": 2022,
                "university_name": "ABC University",
                "university_cgpa_or_percentage": "8.40",
                "university_year": 2025,
                "adhar_card_no": "123456789013",
                "ssmid_no": "12345679",
                "photo": SimpleUploadedFile("create.png", MINIMAL_PNG, content_type="image/png"),
            },
            follow=True,
        )

        self.assertRedirects(response, reverse("admin_dashboard"))
        self.assertContains(response, "Student record for Aman Sharma saved successfully.")
        self.assertTrue(Student.objects.filter(student_no="STU-2002").exists())

    def test_admin_can_edit_student_record(self):
        self.client.login(username="adminuser", password="admin-pass-123")

        response = self.client.post(
            reverse("edit_student", args=[self.student.pk]),
            {
                "name": "Updated Student",
                "gender": self.student.gender,
                "father_name_or_husband_name": self.student.father_name_or_husband_name,
                "father_or_husband_occupation": self.student.father_or_husband_occupation,
                "email_id": self.student.email_id,
                "guardian_phone_no": self.student.guardian_phone_no,
                "permanent_address": self.student.permanent_address,
                "present_address": self.student.present_address,
                "student_no": self.student.student_no,
                "dob": self.student.dob,
                "category": self.student.category,
                "tenth_board_name": self.student.tenth_board_name,
                "tenth_marks": self.student.tenth_marks,
                "tenth_year": self.student.tenth_year,
                "twelfth_board_name": self.student.twelfth_board_name,
                "twelfth_marks": self.student.twelfth_marks,
                "twelfth_year": self.student.twelfth_year,
                "university_name": self.student.university_name,
                "university_cgpa_or_percentage": self.student.university_cgpa_or_percentage,
                "university_year": self.student.university_year,
                "adhar_card_no": self.student.adhar_card_no,
                "ssmid_no": self.student.ssmid_no,
            },
            follow=True,
        )

        self.assertRedirects(response, reverse("admin_dashboard"))
        self.assertContains(response, "Student record for Updated Student updated successfully.")
        self.student.refresh_from_db()
        self.assertEqual(self.student.name, "Updated Student")

    def test_admin_can_delete_student_record(self):
        self.client.login(username="adminuser", password="admin-pass-123")

        response = self.client.post(reverse("delete_student", args=[self.student.pk]), follow=True)

        self.assertRedirects(response, reverse("admin_dashboard"))
        self.assertContains(response, "Student record for Student One deleted successfully.")
        self.assertFalse(Student.objects.filter(pk=self.student.pk).exists())


class SiteSettingsViewTests(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username="siteadmin",
            email="siteadmin@example.com",
            password="admin-pass-123",
        )
        self.admin_user.profile.role = "admin"
        self.admin_user.profile.save()

    def test_admin_can_open_site_settings_page(self):
        self.client.login(username="siteadmin", password="admin-pass-123")

        response = self.client.get(reverse("site_settings"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "site_settings.html")

    def test_admin_dashboard_shows_student_records_for_management(self):
        Student.objects.create(
            name="Managed Student",
            gender="Female",
            father_name_or_husband_name="Parent Name",
            father_or_husband_occupation="Engineer",
            email_id="managed@example.com",
            guardian_phone_no="9876543211",
            permanent_address="Permanent Address",
            present_address="Present Address",
            student_no="STU-3003",
            dob="2005-02-20",
            category="SC",
            tenth_board_name="State Board",
            tenth_marks="82.00",
            tenth_year=2021,
            twelfth_board_name="State Board",
            twelfth_marks="86.00",
            twelfth_year=2023,
            university_name="XYZ University",
            university_cgpa_or_percentage="7.90",
            university_year=2026,
            photo=SimpleUploadedFile("managed.png", MINIMAL_PNG, content_type="image/png"),
            adhar_card_no="123456789099",
            ssmid_no="99887766",
        )
        self.client.login(username="siteadmin", password="admin-pass-123")

        response = self.client.get(reverse("admin_dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Managed Student")
        self.assertContains(response, reverse("edit_student", args=[Student.objects.get(student_no="STU-3003").pk]))


class ContactViewTests(TestCase):
    @override_settings(
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
        CONTACT_EMAIL="contact@example.com",
        DEFAULT_FROM_EMAIL="webmaster@example.com",
    )
    def test_contact_form_sends_message_and_shows_success(self):
        response = self.client.post(
            reverse("contact"),
            {
                "name": "Rakesh",
                "email": "rakesh@example.com",
                "message": "Hello from the contact form",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Message sent successfully.")
        self.assertEqual(len(mail.outbox), 1)

    @override_settings(CONTACT_EMAIL="", DEFAULT_FROM_EMAIL="webmaster@example.com")
    def test_contact_form_shows_error_when_contact_email_missing(self):
        response = self.client.post(
            reverse("contact"),
            {
                "name": "Rakesh",
                "email": "rakesh@example.com",
                "message": "Hello from the contact form",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Contact email is not configured yet.")


class GalleryAdminImageTests(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username="galleryadmin",
            email="galleryadmin@example.com",
            password="admin-pass-123",
        )
        self.admin_user.profile.role = "admin"
        self.admin_user.profile.save()
        self.regular_user = User.objects.create_user(
            username="galleryuser",
            email="galleryuser@example.com",
            password="user-pass-123",
        )
        self.gallery_image = GalleryImage.objects.create(
            title="Campus Day",
            image="gallery/test.png",
            category="Campus",
            description="Original description",
            show_on_home=False,
        )

    def test_admin_can_open_edit_image_page(self):
        self.client.login(username="galleryadmin", password="admin-pass-123")

        response = self.client.get(reverse("edit_image", args=[self.gallery_image.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_image.html")

    def test_admin_can_delete_image(self):
        self.client.login(username="galleryadmin", password="admin-pass-123")

        response = self.client.post(reverse("delete_image", args=[self.gallery_image.pk]))

        self.assertRedirects(response, reverse("gallery"))
        self.assertFalse(GalleryImage.objects.filter(pk=self.gallery_image.pk).exists())

    def test_regular_user_cannot_open_gallery_write_pages(self):
        self.client.login(username="galleryuser", password="user-pass-123")

        upload_response = self.client.get(reverse("upload_image"))
        edit_response = self.client.get(reverse("edit_image", args=[self.gallery_image.pk]))
        delete_response = self.client.get(reverse("delete_image", args=[self.gallery_image.pk]))

        self.assertRedirects(upload_response, reverse("dashboard"))
        self.assertRedirects(edit_response, reverse("dashboard"))
        self.assertRedirects(delete_response, reverse("dashboard"))


class StudentResultAdminTests(TestCase):
    def setUp(self):
        self.admin_view = StudentResultAdmin(StudentResult, admin.site)

    def test_result_status_handles_numeric_marks_stored_as_text(self):
        student = StudentResult(
            name="Pass Case",
            exam_name="Board",
            rank="1",
            marks="85",
            photo="results/test.png",
            year=2025,
        )

        self.assertEqual(self.admin_view.result_status(student), "Pass")

    def test_result_status_handles_invalid_marks_without_crashing(self):
        student = StudentResult(
            name="Unknown Case",
            exam_name="Board",
            rank="1",
            marks="A+",
            photo="results/test.png",
            year=2025,
        )

        self.assertEqual(self.admin_view.result_status(student), "Unknown")


MINIMAL_PNG = (
    b"GIF87a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04\x01"
    b"\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
)


class StudentFormTests(TestCase):
    def test_student_form_sets_12_digit_constraints_for_adhar_widget(self):
        form = StudentForm()

        self.assertEqual(str(form.fields["adhar_card_no"].widget.attrs.get("maxlength")), "12")
        self.assertEqual(str(form.fields["adhar_card_no"].widget.attrs.get("minlength")), "12")
        self.assertEqual(form.fields["adhar_card_no"].widget.attrs.get("inputmode"), "numeric")

    def get_valid_data(self):
        return {
            "name": "Aman Sharma",
            "gender": "Male",
            "father_name_or_husband_name": "Rakesh Sharma",
            "father_or_husband_occupation": "Teacher",
            "email_id": "aman@example.com",
            "guardian_phone_no": "9876543210",
            "permanent_address": "Permanent Address",
            "present_address": "Present Address",
            "student_no": "STU-1001",
            "dob": "2004-01-15",
            "category": "OBC",
            "tenth_board_name": "CBSE",
            "tenth_marks": "88.50",
            "tenth_year": 2020,
            "twelfth_board_name": "CBSE",
            "twelfth_marks": "91.25",
            "twelfth_year": 2022,
            "university_name": "ABC University",
            "university_cgpa_or_percentage": "8.40",
            "university_year": 2025,
            "adhar_card_no": "123456789012",
            "ssmid_no": "12345678",
        }

    def get_photo(self, name="student.png"):
        return SimpleUploadedFile(name, MINIMAL_PNG, content_type="image/png")

    def test_student_form_accepts_valid_data(self):
        form = StudentForm(data=self.get_valid_data(), files={"photo": self.get_photo()})

        self.assertTrue(form.is_valid(), form.errors)

    def test_student_form_rejects_invalid_phone_number(self):
        data = self.get_valid_data()
        data["guardian_phone_no"] = "12AB"

        form = StudentForm(data=data, files={"photo": self.get_photo()})

        self.assertFalse(form.is_valid())
        self.assertIn("guardian_phone_no", form.errors)

    def test_student_unique_constraints_are_enforced(self):
        Student.objects.create(
            **self.get_valid_data(),
            photo=self.get_photo("saved.png"),
        )
        duplicate_data = self.get_valid_data()
        duplicate_data["email_id"] = "other@example.com"

        form = StudentForm(data=duplicate_data, files={"photo": self.get_photo("duplicate.png")})

        self.assertFalse(form.is_valid())
        self.assertIn("student_no", form.errors)

