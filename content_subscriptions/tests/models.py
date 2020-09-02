from django.db import models
from django.contrib.auth.models import AbstractUser

from content_subscriptions.registry import register
from content_subscriptions.models import Subscribable, SubscriptionHolderAddons


class UnsubscribedItem(Subscribable):
    """
    Item that hasn't been registered
    """

    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class ExtendedUser(AbstractUser, SubscriptionHolderAddons):
    """
    User model that has been extended by inheriting SubscriptionHolderAddons Model.
    """

    pass


class Item(Subscribable):
    """
    Item that has been registered.
    """

    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class RandomObject(Subscribable):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


register(Item)
register(RandomObject)
