from django.contrib import admin
from .models import Users, Categories, Images
from .forms import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = Users
    add_form = CustomUserCreationForm

class ImageAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Users, CustomUserAdmin)
admin.site.register(Categories)
admin.site.register(Images, ImageAdmin)