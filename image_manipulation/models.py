from django.db import models
from django.contrib.auth.models import User

# databasee models for images
# Image class instantiates as a row in the table

class Image(models.Model):
  image_path = models.CharField(max_length=1000)
  user = models.ForeignKey(User)
  private = models.BooleanField(default=True)

  def __str__(self):
    return self.image_path

class Meta:
  app_label='stitchpick'
