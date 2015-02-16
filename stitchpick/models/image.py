from django.db import models

# databasee models for images
# Image class instantiates as a row in the table

class Image(models.Model):
  image_path = models.CharField()
  user = models.ForeignKey(User)
  private = models.BooleanField()

class Meta:
  app_label='stitchpick'
