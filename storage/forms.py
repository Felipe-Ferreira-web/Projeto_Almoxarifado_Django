from django.core.exceptions import ValidationError
from django import forms
from storage.models import Item
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation


class ItemForm(forms.ModelForm):

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={"placeholder": "Insira mais detalhes sobre o objeto"}
        ),
        required=False,
        max_length=150,
    )

    is_available = forms.CharField(
        widget=forms.CheckboxInput(),
        help_text="Define se o objeto está disponível para o uso de outros usuários",
        initial=True,
        required=False,
        label="Disponibility",
    )

    storage_location = forms.CharField(
        widget=forms.Select(
            choices=[
                (None, ""),
                ("Pátio 1", "Pátio 1"),
                ("Pátio 2", "Pátio 2"),
                ("Pátio 3", "Pátio 3"),
                ("Armazém", "Armazém"),
            ],
        ),
        label="Storage Location",
    )

    quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={"min": "1", "max": "10"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Item
        fields = (
            "object",
            "quantity",
            "storage_location",
            "is_available",
            "description",
        )

        def clean(self):

            self.add_error(
                "object", ValidationError("Mensagem de erro", code="invalid")
            )
            cleaned_data = self.cleaned_data

            self.add_error()
            return super().clean()


class RegisterForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ["username", "password1", "password2"]:
            self.fields[fieldname].help_text = None

            self.fields["last_name"].label = "Sobrenome"

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            self.add_error(
                "email", ValidationError("Este e-mail já existe!", code="invalid")
            )


class RegisterUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RegisterUpdateForm, self).__init__(*args, **kwargs)

        for fieldname in ["username"]:
            self.fields[fieldname].help_text = None

            self.fields["last_name"].label = "Sobrenome"

    password1 = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=None,
        required=False,
    )

    password2 = forms.CharField(
        label="Confirmar Senha",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=None,
        required=False,
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

        last_name = forms.CharField(label="Sobrenome")

    def clean(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 or password2:
            if password1 != password2:
                self.add_error("password2", ValidationError("As senhas não batem"))
        return super().clean()

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)

        password = self.cleaned_data.get("password1")

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user

    def clean_email(self):
        email = self.cleaned_data.get("email")
        current_email = self.instance.email

        if current_email != email:
            if User.objects.filter(email=email).exists():
                self.add_error(
                    "email", ValidationError("Este e-mail já existe!", code="invalid")
                )
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")

        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as errors:
                self.add_error("password1", ValidationError(errors))

        return password1
