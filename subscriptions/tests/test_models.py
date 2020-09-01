import pytest
import mock

from .conftest import to_list
from ..models import HiddenContent, Subscription, SubscriptionHolderAddons, Subscribable
from django.contrib.contenttypes.models import ContentType


@pytest.mark.django_db
def test_hidden_content_str(user_factory, item_factory):
    user = user_factory.create()
    item = item_factory.create(owner=user)
    h = HiddenContent.objects.create(owner=user, content_object=item)

    string = h.__str__()

    assert string == f'{user.username} is hidding content {item}'


@pytest.mark.django_db
def test_subscription_str(user_factory):
    user1 = user_factory.create()
    user2 = user_factory.create()
    content_type = ContentType.objects.get(model='item')
    s = Subscription.objects.create(subscriber=user2, provider=user1, content_type=content_type)

    string = s.__str__()

    assert string == f'{user2.username} is subscribing to {user1.username}\'s {content_type} content'


@mock.patch('subscriptions.models.subscription_holder_addon.utils')
def test_subscription_holder_addon_subscribe(mock_utils):
    mock_addon = mock.MagicMock(spec=SubscriptionHolderAddons)
    mock_provider = mock.MagicMock()
    mock_content = mock.MagicMock()

    SubscriptionHolderAddons.subscribe(mock_addon, mock_provider, mock_content)

    mock_utils.subscribe.assert_called_with(mock_addon, mock_provider, mock_content)


@mock.patch('subscriptions.models.subscription_holder_addon.utils')
def test_subscription_holder_addon_unsubscribe(mock_utils):
    mock_addon = mock.MagicMock(spec=SubscriptionHolderAddons)
    mock_provider = mock.MagicMock()
    mock_content = mock.MagicMock()

    SubscriptionHolderAddons.unsubscribe(mock_addon, mock_provider, mock_content)

    mock_utils.unsubscribe.assert_called_with(mock_addon, mock_provider, mock_content)


@mock.patch('subscriptions.models.subscription_holder_addon.utils')
def test_subscription_holder_addon_unsubscribe_all(mock_utils):
    mock_addon = mock.MagicMock(spec=SubscriptionHolderAddons)

    SubscriptionHolderAddons.unsubscribe_all(mock_addon)

    mock_utils.unsubscribe_all.assert_called_with(mock_addon)


@mock.patch('subscriptions.models.subscription_holder_addon.utils')
def test_subscription_holder_addon_remove_subscriber(mock_utils):
    mock_addon = mock.MagicMock(spec=SubscriptionHolderAddons)
    mock_subscriber = mock.MagicMock()

    SubscriptionHolderAddons.remove_subscriber(mock_addon, mock_subscriber)

    mock_utils.remove_subscriber.assert_called_with(mock_addon, mock_subscriber)


@mock.patch('subscriptions.models.subscription_holder_addon.utils')
def test_subscription_holder_addon_hide(mock_utils):
    mock_addon = mock.MagicMock(spec=SubscriptionHolderAddons)
    mock_content_object = mock.MagicMock()

    SubscriptionHolderAddons.hide(mock_addon, mock_content_object)

    mock_utils.hide_content.assert_called_with(mock_addon, mock_content_object)


@mock.patch('subscriptions.models.subscription_holder_addon.utils')
def test_subscription_holder_addon_reveal(mock_utils):
    mock_addon = mock.MagicMock(spec=SubscriptionHolderAddons)
    mock_content_object = mock.MagicMock()

    SubscriptionHolderAddons.reveal(mock_addon, mock_content_object)

    mock_utils.reveal_content.assert_called_with(mock_addon, mock_content_object)


@mock.patch('subscriptions.models.subscription_holder_addon.utils')
def test_subscription_holder_get_subscribers(mock_utils):
    mock_addon = mock.MagicMock(spec=SubscriptionHolderAddons)

    SubscriptionHolderAddons.get_subscribers(mock_addon)

    mock_utils.get_subscribers.assert_called_with(mock_addon)


@mock.patch('subscriptions.models.subscription_holder_addon.utils')
def test_subscription_holder_get_subscriptions(mock_utils):
    mock_addon = mock.MagicMock(spec=SubscriptionHolderAddons)

    SubscriptionHolderAddons.get_subscriptions(mock_addon)

    mock_utils.get_subscriptions.assert_called_with(mock_addon)


@mock.patch('subscriptions.models.subscribable.utils')
def test_subscribable_hide(mock_utils):
    mock_subscribable = mock.MagicMock(spec=Subscribable)
    mock_owner = mock.MagicMock()
    mock_subscribable.owner = mock_owner

    Subscribable.hide(mock_subscribable)

    mock_utils.hide_content.assert_called_with(mock_owner, mock_subscribable)


@mock.patch('subscriptions.models.subscribable.utils')
def test_subscribable_reveal(mock_utils):
    mock_subscribable = mock.MagicMock(spec=Subscribable)
    mock_owner = mock.MagicMock()
    mock_subscribable.owner = mock_owner

    Subscribable.reveal(mock_subscribable)

    mock_utils.reveal_content.assert_called_with(mock_owner, mock_subscribable)


@pytest.mark.parametrize('loaded_db, item_idx, expected_users', [
    (None, 0, (1, 2)),
    (None, 1, (1, 2)),
    (None, 2, tuple()),
    (None, 3, tuple()),
    (None, 4, (0, 1)),
    (None, 5, (0, 1))
],
    indirect=['loaded_db'],
    ids=['item0', 'item1', 'item2', 'item3', 'item4', 'item5'])
@pytest.mark.django_db
def test_subscribable_available_to(loaded_db, item_idx, expected_users):
    users, items = loaded_db

    ret_val = to_list(items[item_idx].available_to())

    assert to_list(users[idx] for idx in expected_users) == ret_val


@pytest.mark.parametrize('loaded_db, item_idx, expected_users', [
    (None, 0, (1, 2)),
    (None, 1, (2,)),
    (None, 2, tuple()),
    (None, 3, tuple()),
    (None, 4, (0, 1)),
    (None, 5, (0, 1))
],
    indirect=['loaded_db'],
    ids=['item0', 'item1', 'item2', 'item3', 'item4', 'item5'])
@pytest.mark.django_db
def test_subscribable_visible_to(loaded_db, item_idx, expected_users):
    users, items = loaded_db

    ret_val = to_list(items[item_idx].visible_to())

    assert to_list(users[idx] for idx in expected_users) == ret_val
