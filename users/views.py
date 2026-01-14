from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect, render
from rest_framework import generics, permissions
from .forms import (
    CustomPasswordChangeForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
    SignUpForm,
    UserProfileForm,
)
from .models import UserProfile
from .serializers import UserProfileSerializer


def home(request):
    return render(request, "home.html")


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "成功登入！")
            return redirect("home")
        messages.error(request, "登入失敗，請再試一次。")
        return redirect("login")
    return render(request, "users/login.html")


def logout_user(request):
    logout(request)
    messages.success(request, "您已成功登出。")
    return redirect("home")


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            messages.success(request, "註冊成功！歡迎加入 🐾")
            return redirect("home")
        messages.error(request, "註冊資料有誤，請確認後再送出。")
    else:
        form = SignUpForm()

    return render(request, "users/register.html", {"form": form})


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
        return profile


@login_required(login_url="login")
def user_profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "個人資料已更新。")
            return redirect("user-profile")
        messages.error(request, "更新失敗，請檢查欄位格式。")
    else:
        form = UserProfileForm(instance=profile)

    return render(request, "users/profile.html", {"form": form, "user": request.user})


class CustomPasswordResetView(auth_views.PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = "registration/password_reset.html"


class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "registration/password_reset_done.html"


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = "registration/password_reset_confirm.html"


class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "registration/password_reset_complete.html"


class CustomPasswordChangeView(auth_views.PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = "registration/password_change.html"


class CustomPasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = "registration/password_change_done.html"
