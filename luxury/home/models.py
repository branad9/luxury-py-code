from datetime import datetime
from django.db import models
from django.db.models.query import QuerySet


class SoftDeleteQuerySet(QuerySet):
    def delete(self):
        return super(SoftDeleteQuerySet, self).update(deleted=datetime.now())

    def hard_delete(self):
        return super(SoftDeleteQuerySet, self).delete()

    def restore(self):
        return super(SoftDeleteQuerySet, self).update(deleted=None)   

    def alive(self):
        return self.filter(deleted=None)

    def dead(self):
        return self.exclude(deleted=None)     


class SoftDeleteManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeleteManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeleteQuerySet(self.model).filter(deleted=None)
        return SoftDeleteQuerySet(self.model)

    def delete(self):    
        return self.get_queryset().delete()  

    def hard_delete(self):
        return self.get_queryset().hard_delete()    
    
    def restore(self):
        return self.get_queryset().restore()    


class SoftDeleteModel(models.Model):
    deleted = models.DateTimeField(null=True, blank=True)
    objects = SoftDeleteManager()
    all_objects = SoftDeleteManager(alive_only=False) # models.Manager()

    def delete(self):    
        return SoftDeleteQuerySet(self).update(deleted=datetime.now())

    def hard_delete(self):
        return SoftDeleteQuerySet(self).delete()

    def restore(self):
        return SoftDeleteQuerySet(self).update(deleted=None)     

    class Meta:
        abstract = True


class Settings(models.Model):
    marquee = models.CharField(max_length=250, null=True, blank=True)
    address = models.TextField(max_length=600)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=250)
    whatsapp_phone = models.CharField(max_length=15)
