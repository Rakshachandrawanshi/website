from django import forms

from .models import Company, GalleryImage, Hero, Profile, Student


# Contact Form
class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your name'
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your message',
            'rows': 4
        })
    )


# Profile Form
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['school_name', 'phone', 'image']

        widgets = {
            'school_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter school name'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["name", "tagline", "logo", "favicon", "primary_color", "accent_color", "surface_tint"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter site name"}),
            "tagline": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Enter site tagline", "rows": 3}
            ),
            "logo": forms.FileInput(attrs={"class": "form-control"}),
            "favicon": forms.FileInput(attrs={"class": "form-control"}),
            "primary_color": forms.TextInput(attrs={"class": "form-control form-control-color", "type": "color"}),
            "accent_color": forms.TextInput(attrs={"class": "form-control form-control-color", "type": "color"}),
            "surface_tint": forms.TextInput(attrs={"class": "form-control form-control-color", "type": "color"}),
        }


class HeroForm(forms.ModelForm):
    class Meta:
        model = Hero
        fields = ["title", "subtitle", "button_text", "image", "image_caption"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter hero title"}),
            "subtitle": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Enter hero subtitle", "rows": 4}
            ),
            "button_text": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter hero button text"}
            ),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "image_caption": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Describe the hero image", "rows": 3}
            ),
        }


class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ["title", "category", "description", "show_on_home", "image"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter image title",
            }),
            "category": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. Campus, Event, Results",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Add a short description for this image",
                "rows": 3,
            }),
            "show_on_home": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control",
                "accept": "image/*",
                "id": "imageInput",
            }),
        }


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "name",
            "gender",
            "father_name_or_husband_name",
            "father_or_husband_occupation",
            "email_id",
            "guardian_phone_no",
            "permanent_address",
            "present_address",
            "student_no",
            "dob",
            "category",
            "tenth_board_name",
            "tenth_marks",
            "tenth_year",
            "twelfth_board_name",
            "twelfth_marks",
            "twelfth_year",
            "university_name",
            "university_cgpa_or_percentage",
            "university_year",
            "photo",
            "adhar_card_no",
            "ssmid_no",
        ]
        labels = {
            "name": "Student Name",
            "gender": "Gender",
            "father_name_or_husband_name": "Father / Husband Name",
            "father_or_husband_occupation": "Father / Husband Occupation",
            "email_id": "Email ID",
            "guardian_phone_no": "Guardian Phone Number",
            "permanent_address": "Permanent Address",
            "present_address": "Present Address",
            "student_no": "Student Number",
            "dob": "Date of Birth",
            "category": "Category",
            "tenth_board_name": "10th Board Name",
            "tenth_marks": "10th Marks",
            "tenth_year": "10th Passing Year",
            "twelfth_board_name": "12th Board Name",
            "twelfth_marks": "12th Marks",
            "twelfth_year": "12th Passing Year",
            "university_name": "University Name",
            "university_cgpa_or_percentage": "University CGPA / Percentage",
            "university_year": "University Passing Year",
            "photo": "Student Photo",
            "adhar_card_no": "Adhar Card Number",
            "ssmid_no": "SSMID Number",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter student name"}),
            "gender": forms.Select(attrs={"class": "form-select"}),
            "father_name_or_husband_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter father or husband name"}
            ),
            "father_or_husband_occupation": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter occupation"}
            ),
            "email_id": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter email address"}),
            "guardian_phone_no": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter guardian phone number",
                    "inputmode": "numeric",
                    "maxlength": 15,
                    "minlength": 10,
                    "pattern": r"\+?[0-9]{10,15}",
                }
            ),
            "permanent_address": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Enter permanent address", "rows": 3}
            ),
            "present_address": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Enter present address", "rows": 3}
            ),
            "student_no": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter student number"}),
            "dob": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "tenth_board_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter 10th board name"}
            ),
            "tenth_marks": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "tenth_year": forms.NumberInput(attrs={"class": "form-control"}),
            "twelfth_board_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter 12th board name"}
            ),
            "twelfth_marks": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "twelfth_year": forms.NumberInput(attrs={"class": "form-control"}),
            "university_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter university name"}
            ),
            "university_cgpa_or_percentage": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "university_year": forms.NumberInput(attrs={"class": "form-control"}),
            "photo": forms.ClearableFileInput(attrs={"class": "form-control", "accept": "image/*"}),
            "adhar_card_no": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter 12-digit adhar card number",
                    "inputmode": "numeric",
                    "maxlength": 12,
                    "minlength": 12,
                    "pattern": r"[0-9]{12}",
                }
            ),
            "ssmid_no": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter SSMID number",
                    "inputmode": "numeric",
                    "maxlength": 20,
                    "minlength": 8,
                    "pattern": r"[0-9]{8,20}",
                }
            ),
        }

    def clean_guardian_phone_no(self):
        return self.cleaned_data["guardian_phone_no"].strip()

    def clean_adhar_card_no(self):
        return self.cleaned_data["adhar_card_no"].strip()

    def clean_ssmid_no(self):
        return self.cleaned_data["ssmid_no"].strip()
