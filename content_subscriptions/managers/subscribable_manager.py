from django.db.models import Manager, Q, F
from django.contrib.contenttypes.models import ContentType
from django.apps import apps


class SubscribableManager(Manager):
    use_for_related_fields = True

    def all(self):
        """
        Get all content I own and (that I am subscribed to and is not hidden from me).
        """

        query = self._query_content_owned_by_instance() | \
            (~self._query_content_hidden_by_owner() & self._query_content_from_providers())

        return self.model.objects.filter(query)

    def available(self):
        """
        Get all content that I own and that I am subscribed to and is not hidden from me and that I have not hidden).
        """

        query = self._query_content_owned_by_instance() | \
            (~self._query_content_hidden_by_owner() &
             ~self._query_conent_hidden_by_instance() &
             self._query_content_from_providers())

        return self.model.objects.filter(query)

    def mine(self):
        """
        Get all content that I own.
        """

        return self.get_queryset()

    def receiving(self):
        """
        Get all content that I am subscribed to (including the content I have hidden).
        """

        query = self._query_content_from_providers() & ~self._query_content_hidden_by_owner()
        return self.model.objects.filter(query)

    def sharing(self):
        """
        Get all content that I am sharing.
        """

        return self.get_queryset().exclude(self._query_conent_hidden_by_instance())

    def hiding(self):
        """
        Get all content that I own that I am hiding.
        """

        return self.get_queryset().filter(self._query_conent_hidden_by_instance())

    def hidden(self):
        """
        Get all content that I am subscribed to that I don't want to see.
        """

        return self.receiving().filter(self._query_conent_hidden_by_instance())

    def _query_content_hidden_by_owner(self):
        """
        Returns the query for getting content that has been hidden by its owner.
        """

        return Q(hidden__owner=F('owner'))

    def _query_conent_hidden_by_instance(self):
        """
        Returns the query for getting content that has been hidden by an instance that is not the owner of the content.
        """

        return Q(hidden__owner=self.instance)

    def _query_content_from_providers(self):
        """
        Returns the query for getting content from all the providers subscribed to by an instance.
        """

        subscription = apps.get_model('content_subscriptions', 'Subscription')
        ctype = ContentType.objects.get_for_model(self.model)
        providers = subscription.objects.filter(
            content_type=ctype, subscriber=self.instance.id).prefetch_related('provider__id').values_list('provider__id')
        return Q(owner__in=providers)

    def _query_content_owned_by_instance(self):
        """
        Returns the query for getting the content that is owned by the calling instance.
        """

        return Q(owner=self.instance)
