from typing import Optional

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import signals
from django.utils.translation import gettext_lazy as _

from artists.models import Artist
from utils.models import TimestampedModel


class User(AbstractUser, TimestampedModel):
    class Theme(models.TextChoices):
        LIGHT = "light", _("Light")
        DARK = "dark", _("Dark")

    email_verified = models.BooleanField(default=True)
    preferred_theme = models.CharField(
        max_length=8, choices=Theme.choices, default=Theme.LIGHT
    )

    def save(self, *args, **kwargs):
        if not hasattr(self, "wallet"):
            self.wallet = Wallet(user=self)

        super().save(*args, **kwargs)

    def buy_artist(self, artist: Artist):
        if not artist:
            return

        success = self.wallet.buy(artist.current_price, artist=artist)
        if not success:
            return

        self.label.add_artist(artist)
        return artist

    def sell_artist(self, artist: Artist):
        if not artist:
            return

        success = self.wallet.sell(artist.current_price, artist=artist)
        if not success:
            return

        self.label.artists.remove(artist)
        return artist

    @property
    def has_label(self):
        return RecordLabel.objects.filter(user=self).exists()


class Wallet(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wallet'
    )
    balance = models.PositiveIntegerField(default=1000)

    def sell(
        self, amount: int, notes: Optional[str] = None, artist: Optional[Artist] = None
    ):
        self.balance += amount
        self.save()
        self.transactions.add(
            Transaction(
                transaction_type=Transaction.DEPOSIT,
                amount=amount,
                notes=notes,
                artist=artist,
            ),
            bulk=False,
        )
        return True

    def buy(
        self, amount: int, notes: Optional[str] = None, artist: Optional[Artist] = None
    ):
        if self.balance < amount:
            return False

        self.balance -= amount
        self.save()
        self.transactions.add(
            Transaction(
                transaction_type=Transaction.WITHDRAW,
                amount=amount,
                notes=notes,
                artist=artist,
            ),
            bulk=False,
        )
        return True


class Transaction(models.Model):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"

    TRANSACTION_TYPE = (
        (DEPOSIT, "Venduto"),
        (WITHDRAW, "Acquistato"),
    )

    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name="transactions"
    )
    artist = models.ForeignKey(
        Artist, on_delete=models.SET_NULL, null=True, blank=True, default=None
    )
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE)
    amount = models.IntegerField()
    notes = models.CharField(max_length=256, null=True, blank=True, default=None)
    timestamp = models.DateTimeField(auto_now_add=True)


class RecordLabel(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='label'
    )
    name = models.CharField(max_length=256, null=False, blank=False)
    artists = models.ManyToManyField(Artist)
    slots = models.IntegerField(default=3)

    def __str__(self):
        return f"{self.name} - {self.user}"

    @property
    def slots_available(self) -> int:
        return max(self.slots - self.artists.count(), 0)

    @property
    def is_empty(self) -> bool:
        return self.artists.count() == 0

    def add_artist(self, artist):
        if self.slots_available:
            self.artists.add(artist)


def create_wallet(sender, instance, created, **kwargs):
    """Create Wallet for every new User."""
    if created:
        Wallet.objects.create(user=instance)


signals.post_save.connect(create_wallet, sender=User, weak=False, dispatch_uid='users.models.create_wallet')
