from django.contrib import admin
from .models import SignUp

# Remember this is just for developers!

class SignUpAdmin(admin.ModelAdmin):
    class Meta:
        model = SignUp

admin.site.register(SignUp, SignUpAdmin)

