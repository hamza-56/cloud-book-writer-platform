from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View

from .forms import UserRegisterForm


class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, "users/register.html", {"form": form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Your account has been created. You can now login"
            )
            return redirect("login")

        return render(request, "users/register.html", {"form": form})
