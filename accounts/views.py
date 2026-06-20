from django.shortcuts import render,redirect
from django.contrib import messages
from django.views import View
from .forms import UserRegistrationForm, VerifyCodeForm, UserLoginForm, UserProfileForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
import random
from django.http import JsonResponse
from .models import OtpCode, User, UserProfile
from django.utils import timezone
from datetime import timedelta
from . import tasks
from orders.models import Order
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(100000,999999)
            tasks.send_otp_code.delay(form.cleaned_data['phone'], random_code)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone'], code=random_code)
            request.session["user_registration_info"] = {
                'phone_number': form.cleaned_data['phone'],
                'email': form.cleaned_data['email'],
                'full_name': form.cleaned_data['full_name'],
                'password': form.cleaned_data['password'],
            }
            messages.success(request, 'we sent you a code', 'success')
            return redirect('accounts:verify_code')
        return render(request, self.template_name, {'form': form})


class UserRegistrationVerifyCodeView(View):
    form_class = VerifyCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/verify.html', {'form': form})

    def post(self, request):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                if timezone.now() - code_instance.created > timedelta(minutes=2):
                    code_instance.delete()
                    messages.error(request, 'this code is expired', 'danger')
                    return redirect('accounts:verify_code')
                User.objects.create_user(
                    user_session['phone_number'], user_session['email'],
                    user_session['full_name'], user_session['password']
                )
                code_instance.delete()
                messages.success(request, "you registered.", "success")
                return redirect("home:home")
            else:
                messages.error(request, 'Invalid code', 'danger')
                return redirect('accounts:verify_code')
        return redirect('home:home')


class ResendVerificationCodeView(View):
    def post(self, request):
        user_session = request.session.get('user_registration_info')
        if not user_session or 'phone_number' not in user_session:
            return JsonResponse({'status': 'error', 'message': 'کد وارد نشد.'}, status=400)

        phone = user_session['phone_number']

        OtpCode.objects.filter(phone_number=phone).delete()

        new_code = random.randint(100000, 999999)

        OtpCode.objects.create(
            phone_number=phone,
            code=new_code,
            created=timezone.now()
        )
        tasks.send_otp_code.delay(phone, new_code)
        return JsonResponse({'status': 'ok', 'message': 'کد جدید ارسال شد'})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request,'you logged out','success')
        return redirect('home:home')


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, phone_number=cd['phone'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you logged in', 'success')
                return redirect('home:home')
            messages.error(request, 'invalid credentials', 'danger')
        return render(request, self.template_name, {'form': form})


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        profile, created = UserProfile.objects.get_or_create(user=user)
        orders = Order.objects.filter(user=user, paid=True).order_by('-created')

        context = {
            'user': user,
            'profile': profile,
            'orders': orders,
        }
        return render(request, 'accounts/profile.html', context)


class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        form = UserProfileForm(instance=profile, user=request.user)
        return render(request, 'accounts/profile_edit.html', {'form': form})

    def post(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        form = UserProfileForm(
            request.POST,
            request.FILES,
            instance=profile,
            user=request.user
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'اطلاعات شما با موفقیت به‌روز شد', 'success')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'خطا در ویرایش اطلاعات', 'danger')
            return render(request, 'accounts/profile_edit.html', {'form': form})


class UserPasswordResetView(auth_views.PasswordResetView):
	template_name = "accounts/password_reset_form.html"
	success_url = reverse_lazy("accounts:password_reset_done")
	email_template_name = "accounts/password_reset_email.html"

class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
	template_name = "accounts/password_reset_done.html"


class UserPasswordConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"
    success_url = reverse_lazy("accounts:password_reset_complete")


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"
