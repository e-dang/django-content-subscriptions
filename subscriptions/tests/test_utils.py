import pytest

from subscriptions.models import Subscription, HiddenContent
from django.contrib.contenttypes.models import ContentType
from .models import Item

from ..exceptions import AlreadySubscribed, UnRegisteredContent
from .conftest import to_list
from .. import utils


@pytest.mark.django_db
def test_subscribe(user_factory):
    user1 = user_factory.create()
    user2 = user_factory.create()

    ret_val = [utils.subscribe(user2, user1, 'item')]

    subscription = to_list(Subscription.objects.all())
    assert ret_val == subscription
    assert user1 == subscription[0].provider
    assert user2 == subscription[0].subscriber
    assert len(user1.subscriptions.all()) == 0
    assert len(user2.subscribers.all()) == 0


@pytest.mark.django_db
def test_subscribe_fail_already_subscribed(user_factory):
    user1 = user_factory.create()
    user2 = user_factory.create()
    Subscription.objects.create(subscriber=user2, provider=user1, content_type=ContentType.objects.get(model='item'))

    with pytest.raises(AlreadySubscribed):
        utils.subscribe(user2, user1, 'item')


@pytest.mark.django_db
def test_subscribe_fail_user_dne(user_factory):
    user1 = user_factory.create()
    user2 = user_factory.create()
    user1.delete()

    with pytest.raises(ValueError):
        utils.subscribe(user2, user1, 'item')


@pytest.mark.django_db
def test_unsubscribe(user_factory):
    user1 = user_factory.create()
    user2 = user_factory.create()
    Subscription.objects.create(subscriber=user2, provider=user1, content_type=ContentType.objects.get(model='item'))

    utils.unsubscribe(user2, user1, 'item')

    assert len(Subscription.objects.all()) == 0
    assert len(user1.subscribers.all()) == 0
    assert len(user1.subscriptions.all()) == 0
    assert len(user2.subscribers.all()) == 0
    assert len(user2.subscriptions.all()) == 0


@pytest.mark.django_db
def test_unsubscribe_fail_not_subscribed(user_factory):
    user1 = user_factory.create()
    user2 = user_factory.create()

    with pytest.raises(Subscription.DoesNotExist):
        utils.unsubscribe(user2, user1, 'item')


@pytest.mark.django_db
def test_unsubscribe_all(user_factory):
    num_users = 5
    users = [user_factory.create() for _ in range(num_users)]
    for i in range(num_users - 1):
        Subscription.objects.create(subscriber=users[num_users - 1],
                                    provider=users[i], content_type=ContentType.objects.get(model='item'))

    utils.unsubscribe_all(users[num_users - 1])

    assert len(Subscription.objects.all()) == 0
    for i in range(num_users):
        assert len(users[i].subscribers.all()) == 0
        assert len(users[i].subscriptions.all()) == 0


@pytest.mark.django_db
def test_remove_subscriber(user_factory):
    user1 = user_factory.create()
    user2 = user_factory.create()
    Subscription.objects.create(subscriber=user2, provider=user1, content_type=ContentType.objects.get(model='item'))

    utils.remove_subscriber(user1, user2)

    assert len(Subscription.objects.all()) == 0
    assert len(user1.subscribers.all()) == 0
    assert len(user1.subscriptions.all()) == 0
    assert len(user2.subscribers.all()) == 0
    assert len(user2.subscriptions.all()) == 0


@pytest.mark.django_db
def test_remove_subscriber_from_content_type(user_factory):
    user1 = user_factory.create()
    user2 = user_factory.create()
    Subscription.objects.create(subscriber=user2, provider=user1, content_type=ContentType.objects.get(model='item'))
    s = Subscription.objects.create(subscriber=user2, provider=user1,
                                    content_type=ContentType.objects.get(model='randomobject'))

    utils.remove_subscriber_from_content(user1, user2, 'item')

    subscriptions = Subscription.objects.all()
    assert len(subscriptions) == 1
    assert len(user1.subscribers.all()) == 1
    assert len(user1.subscriptions.all()) == 0
    assert len(user2.subscribers.all()) == 0
    assert len(user2.subscriptions.all()) == 1
    assert subscriptions[0] == s


@pytest.mark.django_db
def test_remove_subscriber_from_content_type_fail_not_subscribed(user_factory):
    user1 = user_factory.create()
    user2 = user_factory.create()

    with pytest.raises(Subscription.DoesNotExist):
        utils.remove_subscriber_from_content(user1, user2, 'item')


@pytest.mark.django_db
def test_hide(user_factory, item_factory):
    user = user_factory.create()
    item = item_factory.create(owner=user)

    ret_val = utils.hide_content(user, item)

    hidden = HiddenContent.objects.all()

    assert len(hidden) == 1
    assert ret_val == hidden[0]
    assert ret_val.content_object == item
    assert ret_val.owner == user


@pytest.mark.django_db
def test_reveal_content(user_factory, item_factory):
    user = user_factory.create()
    item = item_factory.create(owner=user)
    HiddenContent.objects.create(owner=user, content_object=item)

    utils.reveal_content(user, item)

    assert len(HiddenContent.objects.all()) == 0


@pytest.mark.django_db
def test_reveal_content_fail_conent_not_hidden(user_factory, item_factory):
    user = user_factory.create()
    item = item_factory.create(owner=user)

    with pytest.raises(HiddenContent.DoesNotExist):
        utils.reveal_content(user, item)


@pytest.mark.django_db
def test_get_subscribers(user_factory, item_factory):
    user1 = user_factory.create()
    user2 = user_factory.create()
    user3 = user_factory.create()
    _ = item_factory.create(owner=user1)
    content_type = ContentType.objects.get(model='item')
    Subscription.objects.create(subscriber=user2, provider=user1, content_type=content_type)
    Subscription.objects.create(subscriber=user3, provider=user1, content_type=content_type)

    u1_subscribers = utils.get_subscribers(user1)
    u2_subscribers = utils.get_subscribers(user2)
    u3_subscribers = utils.get_subscribers(user3)

    assert u1_subscribers[user2] == [content_type]
    assert u1_subscribers[user3] == [content_type]
    assert len(u2_subscribers) == 0
    assert len(u3_subscribers) == 0


@pytest.mark.django_db
def test_get_subscriptions(user_factory, item_factory):
    user1 = user_factory.create()
    user2 = user_factory.create()
    user3 = user_factory.create()
    _ = item_factory.create(owner=user1)
    content_type = ContentType.objects.get(model='item')
    Subscription.objects.create(subscriber=user2, provider=user1, content_type=content_type)
    Subscription.objects.create(subscriber=user3, provider=user1, content_type=content_type)

    u1_subscriptions = utils.get_subscriptions(user1)
    u2_subscriptions = utils.get_subscriptions(user2)
    u3_subscriptions = utils.get_subscriptions(user3)

    assert u2_subscriptions[user1] == [content_type]
    assert u3_subscriptions[user1] == [content_type]
    assert len(u1_subscriptions) == 0


@pytest.mark.django_db
def test_get_and_check_content_type():
    assert utils.get_and_check_content_type(Item) == ContentType.objects.get(model='item')


@pytest.mark.django_db
def test_get_content_type_fail():
    with pytest.raises(UnRegisteredContent):
        _ = utils.get_and_check_content_type(Subscription)
