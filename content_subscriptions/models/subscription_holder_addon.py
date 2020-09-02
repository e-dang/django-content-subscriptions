from django.db import models
from .. import utils


class SubscriptionHolderAddons(models.Model):
    """
    An abstract model class to add utility functions onto the SUBSCRIPTION_HOLDER_MODEL for convenience
    """

    class Meta:
        abstract = True

    def subscribe(self, content_provider, content_type):
        """
        convenience method that wraps the utility function subscribe
        """

        return utils.subscribe(self, content_provider, content_type)

    def unsubscribe(self, content_provider, content_type):
        """
        convenience method that wraps the utility function unsubscribe
        """

        utils.unsubscribe(self, content_provider, content_type)

    def unsubscribe_all(self):
        """
        convenience method that wraps the utility function unsubscribe_all
        """

        utils.unsubscribe_all(self)

    def remove_subscriber(self, subscriber):
        """
        convenience method that wraps the utility function remove_subscriber
        """

        utils.remove_subscriber(self, subscriber)

    def hide(self, content_object):
        """
        convenience method that wraps the utility function hide
        """

        return utils.hide_content(self, content_object)

    def reveal(self, content_object):
        """
        convenience method that wraps the utility function reveal
        """

        utils.reveal_content(self, content_object)

    def get_subscribers(self):
        """
        convenience method that wraps the utility function get_subscribers
        """

        return utils.get_subscribers(self)

    def get_subscriptions(self):
        """
        convenience method that wraps the utility function get_subscriptions
        """

        return utils.get_subscriptions(self)
