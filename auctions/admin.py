from django.contrib import admin
from .models import Users
from .forms import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = Users
    add_form = CustomUserCreationForm


admin.site.register(Users, CustomUserAdmin)