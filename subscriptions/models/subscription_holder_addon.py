from django.db import models
from .. import utils


class SubscriptionHolderAddons(models.Model):
    """
    An abstract model class to add utility functions onto the SUBSCRIPTION_HOLDER_MODEL for convenience
    """

    class Meta:
        abstract = True

    def subscribe(self, content_provider, content_type):
        return utils.subscribe(self, content_provider, content_type)

    def unsubscribe(self, content_provider, content_type):
        utils.unsubscribe(self, content_provider, content_type)

    def unsubscribe_all(self):
        utils.unsubscribe_all(self)

    def remove_subscriber(self, subscriber):
        utils.remove_subscriber(self, subscriber)

    def hide(self, content_object):
        return utils.hide_content(self, content_object)

    def reveal(self, content_object):
        utils.reveal_content(self, content_object)

    def get_subscribers(self):
        return utils.get_subscribers(self)

    def get_subscriptions(self):
        return utils.get_subscriptions(self)
