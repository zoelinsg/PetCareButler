from django import forms
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm, UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email Address", "autocomplete": "email"}),
    )
    first_name = forms.CharField(
        label="",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name", "autocomplete": "given-name"}),
    )
    last_name = forms.CharField(
        label="",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name", "autocomplete": "family-name"}),
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].label = ""
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "User Name", "autocomplete": "username"}
        )

        self.fields["username"].help_text = None

        for f in ("password1", "password2"):
            self.fields[f].label = ""
            self.fields[f].help_text = None
            self.fields[f].widget.attrs.update(
                {"class": "form-control", "placeholder": "Password" if f == "password1" else "Confirm Password"}
            )

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("此 Email 已被註冊，請改用其他 Email 或使用忘記密碼。")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get("email")
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["phone", "address", "gender", "bio"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone"].widget.attrs.update({"class": "form-control", "placeholder": "輸入電話號碼"})
        self.fields["address"].widget.attrs.update({"class": "form-control", "placeholder": "輸入地址"})
        self.fields["gender"].widget.attrs.update({"class": "form-control"})
        self.fields["bio"].widget.attrs.update({"class": "form-control", "placeholder": "輸入簡介"})


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "請輸入您的電子郵件", "autocomplete": "email"}),
    )


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label="新密碼", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    new_password2 = forms.CharField(label="確認新密碼", widget=forms.PasswordInput(attrs={"class": "form-control"}))


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="舊密碼", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    new_password1 = forms.CharField(label="新密碼", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    new_password2 = forms.CharField(label="確認新密碼", widget=forms.PasswordInput(attrs={"class": "form-control"}))
