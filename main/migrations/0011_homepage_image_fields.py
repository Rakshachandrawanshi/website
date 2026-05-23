from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0010_company_theme_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="galleryimage",
            name="description",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="galleryimage",
            name="show_on_home",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="hero",
            name="image_caption",
            field=models.TextField(blank=True),
        ),
    ]
