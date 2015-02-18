from django.db import models

class Image(models.Model):
  image_path = models.CharField()
  user = models.ForeignKey(User)
  private = models.BooleanField()

  def __str__(self):
    return self.image_path

class Meta:
  app_label='stitchpick'
