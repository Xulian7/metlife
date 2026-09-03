from django import forms
from django.contrib.auth import get_user_model

from .models import ConsultantProfile


class ConsultantCreateForm(forms.ModelForm):
    first_name = forms.CharField(label="Nombres", max_length=150)
    last_name = forms.CharField(label="Apellidos", max_length=150, required=False)
    email = forms.EmailField(label="Email", required=False)
    username = forms.CharField(label="Usuario", max_length=150)

    class Meta:
        model = ConsultantProfile
        fields = ["username", "first_name", "last_name", "email", "role", "phone", "active"]

    def save(self, commit: bool = True):
        User = get_user_model()
        user = User(
            username=self.cleaned_data["username"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data.get("last_name", ""),
            email=self.cleaned_data.get("email", ""),
            is_staff=self.cleaned_data["role"] in {ConsultantProfile.Role.ADMINISTRADOR, ConsultantProfile.Role.DIRECTOR},
        )
        user.set_unusable_password()
        profile = super().save(commit=False)
        profile.user = user
        if commit:
            user.save()
            profile.save()
        return profile
