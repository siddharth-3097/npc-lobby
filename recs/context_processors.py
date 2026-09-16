from django.conf import settings


def posthog(request):
    return {
        "POSTHOG_KEY": settings.POSTHOG_KEY,
        "POSTHOG_HOST": settings.POSTHOG_HOST,
    }
