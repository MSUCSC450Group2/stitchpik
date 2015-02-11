from django.db import models

class User(models.Model):
  username = models.CharField() 

class Meta:
  app_label='stitchpick'
