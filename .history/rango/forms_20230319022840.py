from django import forms
from rango.models import Page, Category
from django.contrib.auth.models import User
from rango.models import UserProfile
from django.contrib.auth.forms import UserCreationForm

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=Category.NAME_MAX_LENGTH, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = Category
        fields = ('name',)
        
class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=Page.TITLE_MAX_LENGTH, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    
    class Meta:
        model = Page
        exclude = ('category',)
        
    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
            
        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url
            
        return cleaned_data
    
class UserCreateForm(UserCreationForm):
    extra_field = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "extra_field", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.extra_field = self.cleaned_data["extra_field"]
        if commit:
            user.save()
        return user
    
# class UserForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput())
    
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password',)
        
# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ('website', 'picture',)