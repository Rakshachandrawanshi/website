from .models import Company, Hero


def site_settings(request):
    return {
        "company": Company.objects.first(),
        "hero": Hero.objects.first(),
    }
