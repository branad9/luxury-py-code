from .models import Settings


def main_settings(request):
    settings = Settings.objects.all()[0]
    return {'cp_settings': settings}
