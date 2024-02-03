from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework.decorators import api_view
from django.views.generic import TemplateView

from .models import Gallery

class GalleryTempateView(TemplateView):
      template_name = 'cms/gallery/index.html'
      

@login_required
@user_passes_test(lambda user: user.is_superadmin)
@api_view(['POST'])
def upload_file(request):
    file = request.FILES.get('file')
    
    try:
        if file:
            if file.content_type.startswith('image'):
                Gallery.objects.create(image=file)
            elif file.content_type.startswith('video'):
                Gallery.objects.create(video=file)
            else:
                return HttpResponse(status=400)
    except Exception as e:
        return HttpResponse(status=500)
    
    return HttpResponse(status=201)


@login_required
@user_passes_test(lambda user: user.is_superadmin)
@api_view(['POST'])
def delete_file(request):
    id = request.POST.get('id')
    
    try:
        if id:
            Gallery.objects.filter(pk=id).delete()
    except:
        return HttpResponse(status=500)

    return HttpResponse(status=201)