from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, AdvocateProfile, Booking, LegalQuery
from django.contrib.auth import authenticate

# --------------------
# Client Registration
# --------------------
class ClientRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    mobile_number = forms.CharField(required=True)
    address = forms.CharField(widget=forms.Textarea)
    state = forms.CharField()
    city = forms.CharField()
    accept_terms = forms.BooleanField()

    class Meta:
        model = User
        fields = ['first_name','last_name','email','mobile_number','address','state','city','password1','password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'client'
        if commit:
            user.save()
        return user

# --------------------
# Advocate Registration
# --------------------


# --------------------
# Login Form
# --------------------
class LoginForm(forms.Form):
    identifier = forms.CharField(label="Email or Mobile")
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        identifier = self.cleaned_data.get('identifier')
        password = self.cleaned_data.get('password')
        user = None
        from .models import User
        if '@' in identifier:
            try:
                user = User.objects.get(email=identifier)
            except User.DoesNotExist:
                pass
        else:
            try:
                user = User.objects.get(mobile_number=identifier)
            except User.DoesNotExist:
                pass
        if user and user.check_password(password):
            self.cleaned_data['user'] = user
        else:
            raise forms.ValidationError("Invalid credentials")
        return self.cleaned_data

# --------------------
# Booking Form
# --------------------
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['service']

# --------------------
# Contact Form
# --------------------
class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    accept_terms = forms.BooleanField()

# --------------------
# Legal Query Form
# --------------------
class LegalQueryForm(forms.ModelForm):
    class Meta:
        model = LegalQuery
        fields = ['question']
