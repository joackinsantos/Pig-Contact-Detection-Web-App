import os

from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class UploadImage(models.Model):
    image = models.ImageField(_("image"),upload_to='pig-images/', null=True, blank=True)  

    def __str__(self):
        return str(os.path.split(self.image.path)[-1])

class DetectedImage(models.Model):
    image = models.ImageField(_("detected-image"),upload_to='detect-images/', null=True, blank=True)  

    def __str__(self):
        return str(os.path.split(self.image.path)[-1])
