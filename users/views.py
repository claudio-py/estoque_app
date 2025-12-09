from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import FormView, ListView, DeleteView,UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from .forms import RegisterUserForm, CustomLoginForm, EditUserForm

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
      user = form.save(commit=False)
      user.image = form.cleaned_data.get("image")
      user.save()
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
        user = self.get_object()

        # prevent self-deletion
        if request.user.id == user.id:
            return redirect("users:list")

        # delete the image file before removing the record
        if user.image:
            user.image.delete(save=False)

        user.delete()
        return redirect("users:list")

class Edit(AdminRequiredMixin, UpdateView):
    model = User
    form_class = EditUserForm
    template_name = "users/edit/index.html"
    context_object_name = "user_obj"

    def form_valid(self, form):
        # keep a reference to the existing image (if any)
        old_image = None
        try:
            old_image = self.get_object().image
        except Exception:
            old_image = None

        # new image (may be None)
        new_image = form.cleaned_data.get("image")

        # Let UpdateView/form save the instance (this writes the new file)
        response = super().form_valid(form)

        # After save: if there was an old image and it's different from the saved one — remove it
        try:
            new_saved_image = self.object.image
        except Exception:
            new_saved_image = None

        if old_image and new_saved_image and old_image.name != new_saved_image.name:
            # delete old file from storage (do not save the model)
            old_image.delete(save=False)

        return response

    def get_success_url(self):
        return reverse_lazy("users:list")
