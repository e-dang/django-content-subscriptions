import pytest
import factory
from pytest_factoryboy import register

from content_subscriptions.tests.models import ExtendedUser, Item
from content_subscriptions.models import Subscription, HiddenContent
from django.contrib.contenttypes.models import ContentType


def to_list(iterable):
    return sorted([data for data in iterable], key=lambda x: x.id)


@register
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ExtendedUser
        django_get_or_create = ('username', 'password')

    username = factory.Sequence(lambda n: f'JohnDoe{n}')
    password = 'thisisatest123'


@register
class ItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Item

    name = factory.Sequence(lambda n: str(n))
    owner = factory.SubFactory(UserFactory)


@pytest.fixture
def loaded_db(db, user_factory, item_factory):
    user0 = user_factory.create()
    user1 = user_factory.create()
    user2 = user_factory.create()

    item0 = item_factory.create(owner=user0)
    item1 = item_factory.create(owner=user0)
    item2 = item_factory.create(owner=user1)
    item3 = item_factory.create(owner=user0)
    item4 = item_factory.create(owner=user2)
    item5 = item_factory.create(owner=user2)

    HiddenContent.objects.create(owner=user0, content_object=item3)
    HiddenContent.objects.create(owner=user1, content_object=item1)

    Subscription.objects.create(subscriber=user1, provider=user0, content_type=ContentType.objects.get(model='item'))
    Subscription.objects.create(subscriber=user1, provider=user2, content_type=ContentType.objects.get(model='item'))
    Subscription.objects.create(subscriber=user2, provider=user0, content_type=ContentType.objects.get(model='item'))
    Subscription.objects.create(subscriber=user0, provider=user2, content_type=ContentType.objects.get(model='item'))

    yield (user0, user1, user2), (item0, item1, item2, item3, item4, item5)
