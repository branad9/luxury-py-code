from .models import Integration, IntegrationPage
from django.urls import resolve

def integration(request):
    if '/cms' in request.path or '/warp' in request.path:
        return {}
    
    all_pages = IntegrationPage.objects.all()
    url_name = resolve(request.path_info).url_name
    pages = [all_pages.get(identifier="*")]    

    for page in all_pages:
        if page.identifier == url_name:
            pages.append(page)

    integrations = Integration.objects.filter(pages__in=pages)
    
    return {'integrations': integrations}