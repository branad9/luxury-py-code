from django.db import models
from home.models import SoftDeleteModel
from PIL import Image
from io import BytesIO
import os.path
from django.core.files.base import ContentFile

class Gallery(SoftDeleteModel):
    image = models.ImageField(upload_to='images/gallery', null=True, blank=True)
    image_thumbnail = models.ImageField(upload_to='images/gallery_thumbnails', null=True, blank=True)
    video = models.FileField(upload_to='videos/gallery', null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.image:
            if not self.make_thumbnail():
                raise Exception('Could not create thumbnail - is the file type valid?')

        super(Gallery, self).save(*args, **kwargs)

    def make_thumbnail(self):
        image = Image.open(self.image)
        image.thumbnail((300, 300), Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(self.image.name)
        thumb_filename = thumb_name + '_thumb' + thumb_extension     

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False 

        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        self.image_thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True


    def __str__(self) -> str:
        return self.image.name or self.video.name
    
    class Meta:
        ordering = ['-created']
        

