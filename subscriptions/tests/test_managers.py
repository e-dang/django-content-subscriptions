import pytest
import mock

from django.contrib.contenttypes.models import ContentType
from .conftest import to_list
from ..managers import SubscriptionManager


@pytest.mark.parametrize('loaded_db, func, user_idx, expected_items_idxs', [
    (None, 'all', 0, (0, 1, 3, 4, 5)),
    (None, 'all', 1, (0, 1, 2, 4, 5)),
    (None, 'all', 2, (0, 1, 4, 5)),
    (None, 'available', 0, (0, 1, 3, 4, 5)),
    (None, 'available', 1, (0, 2, 4, 5)),
    (None, 'available', 2, (0, 1, 4, 5)),
    (None, 'mine', 0, (0, 1, 3)),
    (None, 'mine', 1, (2,)),
    (None, 'mine', 2, (4, 5)),
    (None, 'receiving', 0, (4, 5)),
    (None, 'receiving', 1, (0, 1, 4, 5)),
    (None, 'receiving', 2, (0, 1)),
    (None, 'sharing', 0, (0, 1)),
    (None, 'sharing', 1, (2,)),
    (None, 'sharing', 2, (4, 5)),
    (None, 'hiding', 0, (3,)),
    (None, 'hiding', 1, tuple()),
    (None, 'hiding', 2, tuple()),
    (None, 'hidden', 0, tuple()),
    (None, 'hidden', 1, (1,)),
    (None, 'hidden', 2, tuple())
],
    indirect=['loaded_db'],
    ids=['all_user0', 'all_user1', 'all_user2', 'available_user0', 'available_user1', 'available_user2', 'mine_user0',
         'mine_user1', 'mine_user2', 'receiving_user0', 'receiving_user1', 'receiving_user2', 'sharing_user0',
         'sharing_user1', 'sharing_user2', 'hidding_user0', 'hidding_user1', 'hidding_user2', 'hidden_user0',
         'hidden_user1', 'hidden_user2'])
@pytest.mark.django_db
def test_subscribable_manager(loaded_db, func, user_idx, expected_items_idxs):
    users, items = loaded_db

    ret_items = to_list(getattr(users[user_idx].items, func)())

    assert to_list(items[idx] for idx in expected_items_idxs) == ret_items


@pytest.mark.parametrize('field, expected', [
    ('provider', 'subscriber'),
    ('subscriber', 'provider')
],
    ids=['provider', 'subscriber'])
@pytest.mark.django_db
def test_subscription_manager_get_opposite_field(field, expected):
    mock_manager = mock.MagicMock(spec=SubscriptionManager)

    ret_val = SubscriptionManager._get_opposite_field(mock_manager, field)

    assert ret_val == expected


@pytest.mark.parametrize('loaded_db, related_field, user_idx, expected', [
    (None, 'subscriptions', 0, {2: ['item']}),
    (None, 'subscribers', 0, {1: ['item'], 2: ['item']}),
    (None, 'subscriptions', 1, {0: ['item'], 2:['item']}),
    (None, 'subscribers', 1, {}),
    (None, 'subscriptions', 2, {0: ['item']}),
    (None, 'subscribers', 2, {0: ['item'], 1:['item']}),
], indirect=['loaded_db'],
    ids=['user0_subscriptions', 'user0_subscribers',
         'user1_subscriptions', 'user1_subscribers',
         'user2_subscriptions', 'user2_subscribers'])
@pytest.mark.django_db
def test_subscription_manager_content(loaded_db, related_field, user_idx, expected):
    users, _ = loaded_db

    ret_val = getattr(users[user_idx], related_field).content()

    assert len(ret_val) == len(expected)
    for expected_user_idx, content_types in expected.items():
        assert users[expected_user_idx] in ret_val
        assert to_list(ContentType.objects.get(model=ctype)
                       for ctype in content_types) == to_list(ret_val[users[expected_user_idx]])
