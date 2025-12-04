from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import FormView, ListView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from .forms import RegisterUserForm, CustomLoginForm

User = get_user_model()


class Login(LoginView):
    template_name = "users/login/index.html"
    form_class = CustomLoginForm
    success_url = "/"


class Logout(LogoutView):
    next_page = "/"


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class Register(AdminRequiredMixin, FormView):
    template_name = "users/register/index.html"
    form_class = RegisterUserForm

    def form_valid(self, form):
        user = form.save()
        if user:
            context = self.get_context_data(form=self.form_class())
            context["registered"] = True
            return self.render_to_response(context)
        return self.form_invalid(form)


class List(AdminRequiredMixin, ListView):
    model = User
    template_name = "users/list/index.html"
    context_object_name = "users"
    ordering = ["id"]


class Excluir(AdminRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy("users:list")

    def post(self, request, *args, **kwargs):
        if request.user.id == int(kwargs["pk"]):
            return redirect("users:list")

        response = super().post(request, *args, **kwargs)
        return redirect("users:list")

