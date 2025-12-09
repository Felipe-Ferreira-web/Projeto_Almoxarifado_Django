from django.core.exceptions import ValidationError
from django import forms
from storage.models import Item
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation


class ItemForm(forms.ModelForm):
    """
    Form for creating and updating the Item model.

    Extends ModelForm to customize fields, widgets, and validation logic
    for the Item object, particularly focusing on display, availability,
    and quantity constraints.

    Fields:
    -------
    description : CharField
        Text area for optional, detailed description of the item (max 150 chars).
    is_available : CharField
        Checkbox field to set the item's availability status.
    storage_location : CharField
        Dropdown select field with pre-defined storage location choices.
    quantity : IntegerField
        Numeric input field with range validation (min 1, max 10).
    """

    description = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Insert more details"}),
        required=False,
        max_length=150,
    )

    is_available = forms.CharField(
        widget=forms.CheckboxInput(),
        help_text="Mark if you want the item to be available for other users to borrow.",
        initial=True,
        required=False,
        label="Disponibility",
    )

    storage_location = forms.CharField(
        widget=forms.Select(
            choices=[
                (None, ""),
                ("Storage 1", "Storage 1"),
                ("Storage 2", "Storage 2"),
                ("Storage 3", "Storage 3"),
                ("Warehouse", "Warehouse"),
            ],
        ),
        label="Storage Location",
    )

    quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={"min": "1", "max": "10"}),
    )

    def __init__(self, *args, **kwargs):
        """
        Initializes the ItemForm.

        Ensures the form is correctly bound to the Item instance or prepared
        for creation based on the provided arguments.
        """
        super().__init__(*args, **kwargs)

    class Meta:
        """
        Meta options for the ItemForm.

        Defines the model to be used, the fields to include, and their order.
        """

        model = Item
        fields = (
            "object",
            "quantity",
            "storage_location",
            "is_available",
            "description",
        )

        def clean(self):
            """
            Performs custom validation and cleans the form data.

            This method is responsible for complex validation logic involving
            field dependencies, specifically checking for consistency between quantity and availability.

            Returns
            -------
            dict
            The cleaned and validated data dictionary.
            """

            cleaned_data = super().clean()

            quantity = cleaned_data.get("quantity", 0)
            is_available_checked = cleaned_data.get("is_available")

            if quantity == 0 and is_available_checked:
                self.add_error(
                    "is_available",
                    ValidationError(
                        "Item cannot be available if the quantity is zero.",
                        code="invalid",
                    ),
                )
            return super().clean()


class RegisterForm(UserCreationForm):
    """
    Custom form for registering new users.

    Extends Django's built-in UserCreationForm to include additional user fields
    (first_name, last_name, email) and adds custom validation to ensure the email
    address is unique.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the RegisterForm.

        Removes the default 'help_text' provided by Django for the 'username',
        'password1', and 'password2' fields for a cleaner interface.
        """
        super(RegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ["username", "password1", "password2"]:
            self.fields[fieldname].help_text = None

    class Meta:
        """
        Meta options for the RegisterForm.

        Defines the model to be used (User) and explicitly lists all fields
        to be included in the form.
        """

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
        """
        Custom validation method for the 'email' field.

        Checks if a user with the provided email address already exists in the
        database. If a duplicate is found, a ValidationError is raised.

        Returns
        -------
        str
            The cleaned email address if validation succeeds.

        Raises
        ------
        ValidationError
            If the email address already exists in the User model.
        """
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            self.add_error(
                "email", ValidationError("This email already exist!", code="invalid")
            )


class RegisterUpdateForm(forms.ModelForm):
    """
    Form for updating an existing User's profile data.

    Extends ModelForm to handle non-required password fields, custom password
    matching, password strength validation, and ensuring email uniqueness
    during profile updates.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the RegisterUpdateForm.

        Removes the default 'help_text' for the 'username' field, improving
        the form's clean appearance.
        """
        super(RegisterUpdateForm, self).__init__(*args, **kwargs)

        for fieldname in ["username"]:
            self.fields[fieldname].help_text = None

    password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=None,
        required=False,
    )
    """First password field. Not required for general updates."""

    password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=None,
        required=False,
    )
    """Second password field for confirmation. Not required for general updates."""

    class Meta:
        """
        Meta options for the RegisterUpdateForm.

        Defines the model (User) and includes all editable user fields,
        plus the two custom password fields for update functionality.
        """

        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

    def clean(self):
        """
        Performs cross-field validation.

        Checks if both 'password1' and 'password2' were provided, and if so,
        ensures they match. This prevents partial password submission.

        Returns
        -------
        dict
            The cleaned data dictionary.

        Raises
        ------
        ValidationError
            If the passwords are provided but do not match.
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 or password2:
            if password1 != password2:
                self.add_error(
                    "password2", ValidationError("The passwords are not the same")
                )
        return super().clean()

    def save(self, commit=True):
        """
        Saves the form's data to the User instance.

        If a new password was provided in 'password1', it is hashed using
        user.set_password() before saving the user instance.

        Parameters
        ----------
        commit : bool, optional
            If True, the changes are saved to the database immediately.
            Defaults to True.

        Returns
        -------
        User
            The updated User instance.
        """
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)

        password = self.cleaned_data.get("password1")

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user

    def clean_email(self):
        """
        Custom validation method for the 'email' field during update.

        Ensures that if the email is changed, the new email address does not
        already exist for a *different* user in the database.

        Returns
        -------
        str
            The cleaned email address.

        Raises
        ------
        ValidationError
            If the new email address is already in use by another user.
        """
        email = self.cleaned_data.get("email")
        current_email = self.instance.email

        if current_email != email:
            if User.objects.filter(email=email).exists():
                self.add_error(
                    "email",
                    ValidationError("This E-mail already exist!", code="invalid"),
                )
        return email

    def clean_password1(self):
        """
        Custom validation method for the 'password1' field.

        If a password is provided, it validates the strength against
        Django's configured password validators (e.g., length, complexity).

        Returns
        -------
        str
            The cleaned password value.

        Raises
        ------
        ValidationError
            If the provided password fails any configured strength checks.
        """
        password1 = self.cleaned_data.get("password1")

        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as errors:
                self.add_error("password1", ValidationError(errors))

        return password1
