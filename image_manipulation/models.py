from django.db import models
from django.contrib.auth.models import User
import os

class Image(models.Model):
  imgFile = models.ImageField(upload_to='image/%Y/%m/%d')
  user = models.ForeignKey(User)
  private = models.BooleanField(default=True)

  def userImages(user):
      return Image.objects.filter(user = user)

  def latestUserImageFile(user):
      images = Image.userImages(user)
      return images.reverse()[0].imgFile if images else None

  def resultImageLocation(imgFile, user):
      return 'result_' + user.username + '_' + str(imgFile).split('/')[-1]
    
  def deleteImage(inputImage):
      model = Image.objects.filter(imgFile = str(inputImage)) # database lookup
      if model:
        model.delete()
        os.remove("media/" + str(inputImage))
       
  class Meta:
      app_label = 'image_manipulation'
