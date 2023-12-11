from django import forms
from django.forms import PasswordInput

from mynewsite.models import Category

category_choices = Category.objects.all().values_list('id','name')

class UserSigninForm(forms.Form):
    username = forms.CharField(label="Your name", max_length=100,widget=forms.TextInput(attrs={'class': "form-control", 'style' :'width:45%'}))
    password = forms.CharField(max_length=20, widget=PasswordInput(attrs={'class': "form-control", 'style' :'width:45%'}))
    confirm_password = forms.CharField(max_length=20, widget=PasswordInput(attrs={'class': "form-control", 'style' :'width:45%'}))

class UserRegistrationForm(forms.Form):
    username = forms.CharField(label="Your name", max_length=100, widget=forms.TextInput(attrs={'class': "form-control",'style': 'width:45%'}))
    email = forms.EmailField(label="Your Email address", max_length=100, widget=forms.EmailInput(attrs={'class': "form-control", 'style': 'width:45%'}))
    password = forms.CharField(max_length=20, widget=PasswordInput(attrs={'class': "form-control", 'style': 'width:45%'}))
    confirm_password = forms.CharField(max_length=20, widget=PasswordInput(attrs={'class': "form-control", 'style': 'width:45%'}))

class PostBlog(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    description = forms.CharField(label="Description",widget=forms.Textarea)
    active = forms.BooleanField(required=False)
    image = forms.ImageField()
    category = forms.CharField(label="category", widget=forms.Select(choices=category_choices))
    user = forms.CharField(label="User",widget=forms.HiddenInput, required=False)
    #tags=forms.ModelMultipleChoiceField(queryset=Tag.objects.all())
    status = forms.ChoiceField(choices=(('d', 'Draft'), ('p', 'Published')))

    def __init__(self, *args, **kwargs):
        super(PostBlog, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] ='form-control'


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)