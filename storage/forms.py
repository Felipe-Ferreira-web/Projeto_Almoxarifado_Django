from django.core.exceptions import ValidationError
from django import forms
from storage.models import Item


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
