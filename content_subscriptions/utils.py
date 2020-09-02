"""
Module that contains convenience functions that wrap common database queries.
"""

from .models.subscription import Subscription
from .models.hidden_content import HiddenContent
from django.contrib.contenttypes.models import ContentType
from django.db.utils import IntegrityError
from .exceptions import AlreadySubscribed, UnRegisteredContent
from .registry import registry


def subscribe(subscriber, content_provider, content_type):
    try:
        return Subscription.objects.create(subscriber=subscriber, provider=content_provider,
                                           content_type=get_and_check_content_type(content_type))
    except IntegrityError:
        raise AlreadySubscribed(f'The subscription from {content_provider} to {subscriber} already exists!')
    except ValueError as err:
        raise ValueError(
            f'One to the objects involved in the subscription no longer exist!\nOriginal error: {str(err)}')


def unsubscribe(subscriber, content_provider, content_type):
    Subscription.objects.get(subscriber=subscriber, provider=content_provider,
                             content_type=get_and_check_content_type(content_type)).delete()


def unsubscribe_all(subscriber):
    Subscription.objects.filter(subscriber=subscriber).delete()


def remove_subscriber(provider, subscriber):
    Subscription.objects.filter(subscriber=subscriber, provider=provider).delete()


def remove_subscriber_from_content(provider, subscriber, content_type):
    Subscription.objects.get(subscriber=subscriber, provider=provider,
                             content_type=get_and_check_content_type(content_type)).delete()


def hide_content(owner, content_object):
    return HiddenContent.objects.create(owner=owner, content_object=content_object)


def reveal_content(owner, content_object):
    content_object.hidden.get(owner=owner).delete()


def get_subscribers(subscription_holder):
    return subscription_holder.subscribers.content()


def get_subscriptions(subscription_holder):
    return subscription_holder.subscriptions.content()


def get_and_check_content_type(content_type):
    try:
        ctype = ContentType.objects.get(model=content_type)
    except ContentType.DoesNotExist:
        ctype = ContentType.objects.get(model=content_type._meta.model_name)

    if ctype.model_class() not in registry:
        raise UnRegisteredContent(
            f'The type {ctype.model_class()} has not been registered with the subscribable registry!')

    return ctype
