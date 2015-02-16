from django.db import models


# Create your models here.
class Login(models.Model):
    # can't be blank
    user_name = models.CharField(max_length=50, null=False, blank=False)


    # what shows up in debug and output
    def __string__(self):
        return self.user_name
 
