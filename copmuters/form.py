
from .models import *
from django import forms



class RegistrationForm(forms.Form):
    username = forms.CharField(min_length=1, label='Логин')
    password = forms.CharField(min_length=1, widget=forms.PasswordInput, label='Пароль')
    password2 = forms.CharField(min_length=1, widget=forms.PasswordInput, label='Повторите ввод')

    email = forms.EmailField(label='Email')
    last_name = forms.CharField(label='Фамилия')
    first_name = forms.CharField(label='Имя')
    # avatar = forms.ImageField(label='Аватар', required=False)

class ComputerForm(forms.ModelForm):
    class Meta(object):
        model = Computer
        fields = ['name', 'price', 'pic', 'description', 'quantity', 'type']

    def save(self):
        computer = Computer()
        computer.name = self.cleaned_data.get('name')
        computer.price = self.cleaned_data.get('price')
        computer.type = self.cleaned_data.get('type')
        computer.quantity = self.cleaned_data.get('quantity')
        computer.description = self.cleaned_data.get('description')
        f = self.cleaned_data.get('pic')
        computer.pic = f
        computer.save()

class AnswerForm(forms.Form):
    text = forms.CharField(max_length=100, widget=forms.Textarea(attrs={'class': 'form-control'}))
class SettingForm(forms.Form):
    password = forms.CharField(min_length=8, widget=forms.PasswordInput, label='password')
    password2 = forms.CharField(min_length=8, widget=forms.PasswordInput, label='new password')


class AuthorizationForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')