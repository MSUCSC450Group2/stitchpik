from django.contrib import admin
from .models import SignUp

# Remember this is just for developers!

class LoginAdmin(admin.ModelAdmin):
    class Meta:
        model = Login

admin.site.register(Login, LoginAdmin)

