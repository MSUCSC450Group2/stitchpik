from django.db import models
from django.contrib.auth.models import User

class Image(models.Model):
  imgFile = models.ImageField(upload_to='images/%Y/%m/%d')
  user = models.ForeignKey(User)
  private = models.BooleanField(default=True)

  class Meta:
      app_label = 'image_manipulation'
