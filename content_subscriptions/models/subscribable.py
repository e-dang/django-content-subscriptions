from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from .hidden_content import HiddenContent
from .subscription import Subscription
from .. import utils
from django.apps import apps


class Subscribable(models.Model):
    """
    Abstract model class that any subscribable model should inherit from.
    """

    owner = models.ForeignKey(settings.SUBSCRIPTION_HOLDER_MODEL, related_name='%(class)ss', on_delete=models.CASCADE)
    hidden = GenericRelation(HiddenContent, related_query_name='%(class)s')

    objects = models.Manager()

    class Meta:
        abstract = True

    def hide(self):
        """
        Causes the content to be hidden.
        """

        return utils.hide_content(self.owner, self)

    def reveal(self):
        """
        Unhides the content if it is hidden, otherwise it raises an HiddenContent.DoesNotExist exception.
        """

        utils.reveal_content(self.owner, self)

    def visible_to(self):
        """
        If the owner of the content is not hidding this item, then return a queryset of SUBSCRIPTION_HOLDER_MODELS who
        are subscribed to the provider of this content and have no hidden the content themselves. The queryset never
        contains the owner of the content.
        """

        hidden = self.hidden.values_list('owner')
        return self.available_to().exclude(id__in=hidden)

    def available_to(self):
        """
        If the owner of the content is not hidding this item, then return a queryset of SUBSCRIPTION_HOLDER_MODELS who
        are subscribed to the provider of this content, even if those subscribers have hidden the content themselves.
        The queryset never contains the owner of the content.
        """

        model = apps.get_model(settings.SUBSCRIPTION_HOLDER_MODEL)

        if self.hidden.filter(owner=self.owner).exists():
            return model.objects.none()

        subscribers = Subscription.objects.filter(provider=self.owner).prefetch_related(
            'subscriber').values_list('subscriber', flat=True)
        return model.objects.filter(id__in=subscribers)
