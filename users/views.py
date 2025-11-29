from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import FormView
from .forms import RegisterUserForm


# Create your views here.
class Login(LoginView):
    template_name = "users/login/index.html"
    success_url = "/"


class Logout(LogoutView):
    next_page = "/"


class Register(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = "users/register/index.html"
    form_class = RegisterUserForm
    success_url = "/users/login/"

    # redirect to Django admin login
    login_url = "/admin/login/"
    redirect_field_name = None  # optional: avoid ?next= in URL

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return super().handle_no_permission()

    def form_valid(self, form):
        user = form.save()
        if user:
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
