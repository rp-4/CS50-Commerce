from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Users, Categories


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Users
        fields = "__all__"

def get_categories():
    categories = Categories.objects.all()

    category_names = []

    for c in categories:
        category_names.append((c.category, c.category.title()))
    return category_names

class NewListingForm(forms.Form):

    new_title = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}))

    categories = forms.ChoiceField(
        required=False,
        widget=forms.Select,
        choices= get_categories,
    )

    new_description = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}))
    price = forms.IntegerField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Price'}))


class ModifyListingForm(NewListingForm):
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('deleted', 'Deleted'),
    ]

    status = forms.ChoiceField(
        required=False,
        widget=forms.RadioSelect,
        choices= STATUS_CHOICES,
    )