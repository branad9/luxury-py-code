from django.db import models

from home.models import SoftDeleteModel

class IntegrationPage(SoftDeleteModel):
    identifier = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Integration(SoftDeleteModel):
    pages = models.ManyToManyField(IntegrationPage, related_name="integrations")
    head_code = models.TextField(null=True, blank=True)
    body_code = models.TextField(null=True, blank=True)
    footer_code = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-id']
    
