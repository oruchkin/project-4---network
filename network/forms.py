from django import forms
from django.forms import fields
from . models import Post, User


class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['post_pub_date', 'post_author']
        
        widgets = {                        
            'post_text': forms.Textarea(attrs={"class": "form-control"}),            
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['image', 'about']
        widgets = {
            'about': forms.Textarea(attrs={"class": "form-control"}),
            'image': forms.TextInput(attrs={"class": "form-control"}),
        }
