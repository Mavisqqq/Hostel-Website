from django.contrib.auth.forms import *
from hostel.models import *


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(required=True, label='Имя пользователя', min_length=5, max_length=50, help_text='Максимум 50 символов', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    email = forms.EmailField(required=True, label='E-Mail', widget=forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    password1 = forms.CharField(required=True, label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(required=True, label='Подтвердите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    email = forms.EmailField(label="E-Mail", widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    field_order = ['email', 'password']

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        # remove username
        self.fields.pop('username')

    def clean(self):
        user = User.objects.get(email=self.cleaned_data.get('email'))
        self.cleaned_data['username'] = user.username
        return super(UserLoginForm, self).clean()


class UserForgotPasswordForm(PasswordResetForm):
    #Запрос на восстановление пароля
    def __init__(self, *args, **kwargs):
        #Обновление стилей формы
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })


class UserSetNewPasswordForm(SetPasswordForm):
    #Изменение пароля пользователя после подтверждения
    def __init__(self, *args, **kwargs):
       # Обновление стилей формы
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })


class DateInput(forms.DateInput):
    input_type = 'date'


class DutyForm(forms.ModelForm):
    duty_date = forms.DateField(required=True, label='Дата', widget=DateInput)
    room = forms.CharField(required=True, label='Номер комнаты', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    responsible_person = forms.CharField(required=True, label='Ответственный человек', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    field_order = ['duty_date', 'room', 'responsible_user']

    class Meta:
        model = Duty
        fields = ('responsible_person', 'duty_date', 'room')


class AdForm(forms.ModelForm):
    title = forms.CharField(max_length=150, label='Название', widget=forms.TextInput(attrs={"class": "form-control"}))
    content = forms.CharField(label='Текст', widget=forms.Textarea(attrs={"class": "form-control"}))

    class Meta:
        model = Ads
        fields = ('title', 'content')


class NewsForm(forms.ModelForm):
    title = forms.CharField(max_length=150, label='Название', widget=forms.TextInput(attrs={"class": "form-control"}))
    content = forms.CharField(label='Текст', widget=forms.Textarea(attrs={"class": "form-control"}))

    class Meta:
        model = News
        fields = ('title', 'content')
