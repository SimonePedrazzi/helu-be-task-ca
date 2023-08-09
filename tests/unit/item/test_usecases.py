from dataclasses import asdict
import pytest
from be_task_ca.item.usecases import create_item, get_all, ItemAlreadyExistsError
from be_task_ca.item.interfaces import ItemRepositoryInterface
from be_task_ca.item.model import Item
from be_task_ca.item.schema import (
    AllItemsResponse,
    CreateItemRequest,
    CreateItemResponse,
)
from uuid import uuid4

SAMPLE_UUID = uuid4()


@pytest.fixture
def repo_mock(mocker):
    return mocker.Mock(spec=ItemRepositoryInterface)


class TestCreateItem:
    def test_raises_item_exists_error(self, repo_mock):
        # given
        item = Item(
            id=SAMPLE_UUID,
            name="foo",
            description="lorem ipsum",
            price=9.99,
            quantity=3,
        )
        repo_mock.find_item_by_name.return_value = item
        # then when
        item_request = CreateItemRequest(name=item.name, price=10.5, quantity=1)
        msg = "An item with this name already exists"
        with pytest.raises(ItemAlreadyExistsError, match=msg):
            create_item(item=item_request, repo=repo_mock)
        repo_mock.find_item_by_name.assert_called_once_with(item_request.name)
        repo_mock.save_item.assert_not_called()

    def test_saves_item(self, mocker, repo_mock):
        # given
        mocker.patch("be_task_ca.item.usecases.uuid4", return_value=SAMPLE_UUID)
        repo_mock.find_item_by_name.return_value = None
        # when
        item_request = CreateItemRequest(name="qwerty", price=10.5, quantity=1)
        result = create_item(item=item_request, repo=repo_mock)
        # then
        expected_item = Item(
            id=SAMPLE_UUID,
            name=item_request.name,
            description=item_request.description,
            price=item_request.price,
            quantity=item_request.quantity,
        )
        expected = CreateItemResponse(**asdict(expected_item))
        assert result == expected
        repo_mock.find_item_by_name.assert_called_once_with(item_request.name)
        repo_mock.save_item.assert_called_once_with(expected_item)


class TestGetAll:
    @pytest.mark.parametrize(
        "items",
        [
            pytest.param([]),
            pytest.param(
                [
                    Item(
                        id=uuid4(),
                        name=f"name-{i}",
                        description=f"descr-{i}",
                        price=10 * (i + 1),
                        quantity=i + 1,
                    )
                    for i in range(3)
                ]
            ),
        ],
    )
    def test_returns_response(self, repo_mock, items):
        # given
        repo_mock.get_all_items.return_value = items
        # when
        result = get_all(repo_mock)
        # then
        expected = AllItemsResponse(
            items=[CreateItemResponse(**asdict(x)) for x in items]
        )
        assert result == expected
