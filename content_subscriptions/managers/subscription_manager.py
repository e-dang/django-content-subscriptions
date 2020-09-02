from django.db import models
from collections import defaultdict


class SubscriptionManager(models.Manager):

    use_for_related_fields = True

    def content(self):
        """
        Returns a dictionary containing the SUBSCRIPTION_HOLDER_MODELS that either the calling instance is subscribed to
        or are subscribers of the calling instance as keys and the types of content they are subscribed to as values.
        """

        contents = defaultdict(list)
        for subscription in self.get_queryset():
            contents[getattr(subscription, self._get_opposite_field(self.field.name))].append(subscription.content_type)

        return contents

    def _get_opposite_field(self, field):
        """
        Method for getting the opposite related name on the Subscription model than what the current instance was called
        with.
        """

        return 'subscriber' if field == 'provider' else 'provider'
