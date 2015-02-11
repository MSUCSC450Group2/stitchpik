from django.db import models


# Create your models here.
class SignUp(models.Model):
    # can't be blank
    user_name = models.CharField(max_length=50, null=False, blank=False)
    #last_name = models.CharField(null=True, blank=True)
    #first_name = models.CharField(null=True, blank=True)
    #email = models.EmailField()
    #when created make note of time but not when updated
    #timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    #only note time when updated
    #updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    # what shows up in debug and output
    def __string__(self):
        return self.user_name
 
