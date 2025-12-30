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
    current_loan : ForeignKey
        Link to the current active Transaction record. This allows 1-step
        access to the current borrower without expensive database lookups.
    """

    item_id = models.BigAutoField(primary_key=True)
    object = models.CharField(max_length=20)
    description = models.CharField()
    quantity = models.IntegerField(default=1)
    storage_location = models.CharField()
    is_available = models.BooleanField()
    created_date = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    current_loan = models.ForeignKey(
        "Transaction",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="item_currently_assigned",
    )

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
    receiving/borrowing the item, and the timing of the transfer. This model
    serves as the historical log, while its instances may be referenced by
    the Item model's 'current_loan' field to indicate an active status.

    Attributes:
    -----------
    id : BigAutoField
        The primary key for the transaction record.
    LOAN : str
        Constant representing an item being lent out.
    DEVOLUTION : str
        Constant representing an item being returned.
    item : ForeignKey
        Link to the Item model that is being transacted.
        Note: An active LOAN transaction is linked back via Item.current_loan.
    from_user : ForeignKey
        The User initiating the transfer (owner during LOAN, borrower during DEVOLUTION).
    to_user : ForeignKey
        The User receiving the transfer (borrower during LOAN, owner during DEVOLUTION).
    was_available : BooleanField
        Records the availability status of the item *before* this transaction occurred.
    type : CharField
        The nature of the transaction ('loan' or 'devolution').
    loan_date : DateTimeField
        Timestamp of when the transaction record was created.
    returned_date : DateTimeField
        Timestamp of when the item was returned (specifically for DEVOLUTION records).
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
