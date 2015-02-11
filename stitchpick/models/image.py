from django.db import models

class Image(models.Model):
  image_path = models.CharField()
  user = models.ForeignKey(User)
  private = models.BooleanField()

class Meta:
  app_label='stitchpick'
