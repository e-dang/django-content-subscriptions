from django.db import models
from collections import defaultdict


class SubscriptionManager(models.Manager):

    use_for_related_fields = True

    def content(self):
        contents = defaultdict(list)
        for subscription in self.get_queryset():
            contents[getattr(subscription, self._get_opposite_field(self.field.name))].append(subscription.content_type)

        return contents

    def _get_opposite_field(self, field):
        return 'subscriber' if field == 'provider' else 'provider'
