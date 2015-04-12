from django.db import models
from django.contrib.auth.models import User

class Image(models.Model):
  imgFile = models.ImageField(upload_to='image/%Y/%m/%d')
  user = models.ForeignKey(User)
  private = models.BooleanField(default=True)

  def userImages(user):
      return Image.objects.filter(user = user)

  def latestUserImageFile(user):
      images = Image.userImages(user)
      return images.reverse()[0].imgFile if images else None

  class Meta:
      app_label = 'image_manipulation'
