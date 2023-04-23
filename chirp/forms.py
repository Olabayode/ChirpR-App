from .models import Comment
from django.forms import ModelForm
from django import forms



class CommentForm(ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'
    body = forms.CharField(label='', widget=forms.TextInput(attrs={"class": "bg-transparent max-h-10 shadow-none", "type": "text", "placeholder": "post a comment"}))
    
    class Meta:
        model = Comment
        fields = ['body', 'post', 'user', 'parent']
        widgets = {
            'user': forms.HiddenInput(),
            'post': forms.HiddenInput(),
            'parent': forms.HiddenInput(),
            'body': forms.TextInput(
                attrs={
                    "class": "bg-transparent max-h-10 shadow-none", 
                    "type": "text", 
                    "placeholder": "post a comment"
                }
            )
        }