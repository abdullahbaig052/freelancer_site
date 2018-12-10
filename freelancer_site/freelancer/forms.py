from django import forms
from django.contrib.auth.forms import UserCreationForm, get_user_model
from freelancer.models import AppUser, Project, Bids
import freelancer.messages as msg

class SignUpForm(UserCreationForm):
    CHOICES = [
        ('work', 'I want to work'),
        ('hire', 'I want to hire')
    ]
    user_type = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

    class Meta:
        model = AppUser
        fields = ('user_type', 'username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class UserProfileEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileEditForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['email'].required = True

    class Meta:
        model = AppUser
        fields = ('email', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return self.email_exists(email)

    def save(self, commit=True):
        user = super(UserProfileEditForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

    def email_exists(self, email):
        if email and not (self.instance.email == email) and AppUser.objects.filter(email=email).count():
            raise forms.ValidationError(msg.EMAIL_ALREADY_EXISTS)
        return email


class LoginForm(forms.Form):
    username = forms.CharField(label="username", max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)


class PostProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'budget', )
        widgets = {
            'description': forms.Textarea(attrs={'rows': 7, 'cols': 25}),
        }


class UserBidsForm(forms.ModelForm):
    class Meta:
        model = Bids
        fields = ("cover_letter", "bid_amount")
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 7, 'cols': 25}),
        }


class StatusForm(forms.Form):
    CHOICES = [
        ('Select', 'Select'),
        ('Pending', 'Pending'),
        ('Approve', 'Approve')
    ]
    status = forms.ChoiceField(choices=CHOICES,
                               widget=forms.Select(attrs={'onchange': 'this.form.submit();'}))
