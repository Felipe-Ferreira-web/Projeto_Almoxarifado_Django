from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Item(models.Model):
    """
    Represents a tangible item or asset within the storage system.

    Tracks item details, location, availability status, creation date,
    and the user who owns it. It also calculates which user currently
    holds the item if it's on loan.

    Attributes:
    -----------
    item_id : BigAutoField
        The primary key for the item. Automatically increments and identifies the item.
    object : CharField
        The name or type of the item (max 20 characters).
    description : CharField
        Detailed text describing the item.
    quantity : IntegerField
        The count of this item currently available (defaults to 1).
    storage_location : CharField
        The designated physical location where the item is stored.
    is_available : BooleanField
        Indicates whether the item is currently available for borrowing (True/False).
    created_date : DateTimeField
        The date and time when the item record was created (defaults to current time).
    owner : ForeignKey
        Link to the User model, identifying the user who owns the item.
        If the linked user is deleted, the field is set to NULL.
    """

    item_id = models.BigAutoField(primary_key=True)
    object = models.CharField(max_length=20)
    description = models.CharField()
    quantity = models.IntegerField(default=1)
    storage_location = models.CharField()
    is_available = models.BooleanField()
    created_date = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    @property
    def current_user(self):
        """
        Property to determine the user currently holding the item.

        If the item is available (is_available=True), returns None.
        Otherwise, queries the related Transaction model (assuming a reverse
        relationship 'transaction_item' exists) to find the most recent
        active 'loan' transaction and returns the borrower (to_user).

        Returns
        -------
        User or None
            The User instance currently holding the item, or None if the item is
            available or no active loan record is found.
        """

        if self.is_available:
            return None

        try:
            active_loan = (
                self.transaction_item.filter(type="loan").order_by("-loan_date").first()
            )
            return active_loan.to_user if active_loan else None

        except Exception:
            return None

    def __str__(self) -> str:
        """
        String representation of the Item object.

        Returns
        -------
        str
            The item's description.
        """
        return f"{self.description}"


class Transaction(models.Model):
    """
    Records the history of item loans and devolutions (returns) within the system.

    Tracks the item involved, the user lending/returning the item, the user
    receiving/borrowing the item, and the status/timing of the transfer.

    Attributes:
    -----------
    id : BigAutoField
        The primary key for the transaction record.
    LOAN : str
        Constant representing an item being lent out.
    DEVOLUTION : str
        Constant representing an item being returned.
    item : ForeignKey
        Link to the Item model that is being transacted. Set to NULL if the item is deleted.
    from_user : ForeignKey
        The User who is initiating the transfer (e.g., the owner during a LOAN, or the borrower during a DEVOLUTION).
    to_user : ForeignKey
        The User who is receiving the transfer (e.g., the borrower during a LOAN, or the owner during a DEVOLUTION).
    was_available : BooleanField
        Records the availability status of the item *before* this transaction occurred (defaults to True).
    transaction_types : list of tuple
        Choices available for the 'type' field ('loan' or 'devolution').
    type : CharField
        The nature of the transaction, restricted to 'loan' or 'devolution'.
    loan_date : DateTimeField
        The date and time the transaction record was created (defaulting to the current time).
    returned_date : DateTimeField
        The date and time the item was returned (used only for DEVOLUTION records).
    """

    id = models.BigAutoField(primary_key=True)
    LOAN = "loan"
    DEVOLUTION = "devolution"
    item = models.ForeignKey(
        Item,
        on_delete=models.SET_NULL,
        null=True,
        related_name="transaction_item",
    )
    from_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="transaction_given",
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="transaction_received",
    )
    was_available = models.BooleanField(default=True)

    transaction_types = [(LOAN, "Loan"), (DEVOLUTION, "Devolution")]
    type = models.CharField(max_length=10, choices=transaction_types, default=LOAN)

    loan_date = models.DateTimeField(default=timezone.now)
    returned_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        """
        Meta options for the Transaction model.

        Defines the default ordering for querysets of this model.
        """

        ordering = ["-loan_date"]

    def __str__(self):
        """
        String representation of the Transaction object.

        Returns
        -------
        str
            A formatted string including the transaction ID and the item description.
        """
        return f"Transaction #{self.id} | {self.item if self.item else "NO Item"}"
