from django.db import models

class User(models.Model):
  username = models.CharField() 

  def __str__(self):
    return self.username

class Meta:
  app_label='stitchpick'
