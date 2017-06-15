from material import Layout, Row, Fieldset
from django import forms

class RegistrationForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField(label="Email Address")
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm password")
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    gender = forms.CharField(required=False)
    receive_news = forms.BooleanField(required=True, label="I want to receive news")
    agree_toc = forms.BooleanField(required=True, label="I agree wit hthe Terms and Conditions")
    
    layout = Layout('username', 'email',
        Row('password', 'password_confirm'),
        Fieldset('Personal details',
            Row('first_name', 'last_name'),
            'gender', 'receive_news', 'agree_toc'))
