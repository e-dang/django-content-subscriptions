from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from ..managers.subscription_manager import SubscriptionManager


class Subscription(models.Model):
    """
    Holds the relationship between the SUBSCRIPTION_HOLDER_MODEL's and the content type that is being subscribed to.
    """

    subscriber = models.ForeignKey(settings.SUBSCRIPTION_HOLDER_MODEL,
                                   related_name='subscriptions', on_delete=models.CASCADE)
    provider = models.ForeignKey(settings.SUBSCRIPTION_HOLDER_MODEL,
                                 related_name='subscribers', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    objects = models.Manager()
    subscription_manager = SubscriptionManager()

    class Meta:
        default_manager_name = 'subscription_manager'
        unique_together = ['subscriber', 'provider', 'content_type']

    def __str__(self):
        return f'{self.subscriber.username} is subscribing to {self.provider.username}\'s {self.content_type} content'
