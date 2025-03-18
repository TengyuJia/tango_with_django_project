from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User
from rango.models import Page, Category, UserProfile,Comment, RecommendedDish, Rating, Price
class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=Category.Name_Max_Length,
                            help_text = 'Please enter the category name.')
    views = forms.IntegerField(widget=forms.HiddenInput(), initial = 0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial = 0)
    slug = forms.SlugField(widget = forms.HiddenInput(), required=False)
    class Meta:
        model = Category
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        
class PageForm(forms.ModelForm):
    title = forms.CharField(max_length = 128,
                            help_text="Please enter the name of the restaurant.")
    url = forms.CharField(max_length = 200,
                        help_text="Please enter the official website of the restaurant.")
    location = forms.CharField(max_length = 128,
                            help_text="Please enter the location of the restaurant.")                             
    slug = forms.SlugField(widget = forms.HiddenInput(), required=False)                   
    views = forms.IntegerField(widget=forms.HiddenInput(), initial= 0)
    price = forms.IntegerField(initial= 0, help_text="Please enter the price per person of the restaurant.") 
    image = forms.ImageField(required=False, help_text="Upload an image of the restaurant.")
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial = 0)
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        
# 用户注册表单
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

# 用户登录表单
class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

# 用户资料表单
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

# 修改密码表单（继承自 Django 内置的 PasswordChangeForm）
class UserPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class RecommendedDishForm(forms.ModelForm):
    class Meta:
        model = RecommendedDish
        fields = ['dish_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        
class PriceForm(forms.ModelForm):
    class Meta:
        model = Price
        fields = ['price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['stars']
        widgets = {
            'stars': forms.NumberInput(attrs={'min': 0, 'max': 5, 'step': 0.5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'