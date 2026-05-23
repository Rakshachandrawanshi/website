from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0011_homepage_image_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="company",
            name="favicon",
            field=models.ImageField(blank=True, null=True, upload_to="company/"),
        ),
    ]
