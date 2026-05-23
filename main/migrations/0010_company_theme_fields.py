from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0009_company_logo_galleryimage_category_hero_button_text_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="company",
            name="accent_color",
            field=models.CharField(default="#2850af", max_length=7),
        ),
        migrations.AddField(
            model_name="company",
            name="primary_color",
            field=models.CharField(default="#17378f", max_length=7),
        ),
        migrations.AddField(
            model_name="company",
            name="surface_tint",
            field=models.CharField(default="#f4f8ff", max_length=7),
        ),
    ]
