from uuid import uuid4
from be_task_ca.item.model import Item
from be_task_ca.item.repository import SqlItemRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest


def item_factory(**kwargs) -> Item:
    defaults = {
        "id": uuid4(),
        "name": "abc",
        "description": "lorem ipsum",
        "price": 10,
        "quantity": 3,
    }
    return Item(**(defaults | kwargs))


@pytest.fixture(scope="session")
def db():
    engine = create_engine("postgresql://postgres:example@localhost:5432/postgres")
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)()


@pytest.fixture(autouse=True)
def reset_tables(db):
    yield
    db.query(Item).delete()
    db.commit()


@pytest.fixture
def repo(db):
    return SqlItemRepository(db=db)


class TestFindItemByName:
    @pytest.mark.parametrize(
        "items_kwargs",
        [
            pytest.param([]),
            pytest.param(
                [{"name": name} for name in ["foo", "bar", "baz"]],
            ),
        ],
    )
    @pytest.mark.parametrize(
        "name_searched",
        [
            "notexists",
            "bar",
        ],
    )
    def test_returns_expected_item(self, db, repo, items_kwargs, name_searched):
        # given
        items = []
        if items_kwargs:
            items = [item_factory(**x) for x in items_kwargs]
            for item in items:
                db.add(item)
            db.commit()
        # when
        result = repo.find_item_by_name(name=name_searched)
        # then
        expected = next((x for x in items if x.name == name_searched), None)
        assert result == expected


class TestGetAllItems:
    @pytest.mark.parametrize(
        "items_kwargs",
        [
            pytest.param([]),
            pytest.param([{"name": f"name-{i}"} for i in range(3)]),
        ],
    )
    def test_returns_all_items(self, db, repo, items_kwargs):
        # given
        items = []
        if items_kwargs:
            items = [item_factory(**x) for x in items_kwargs]
            for item in items:
                db.add(item)
            db.commit()
        # when
        result = repo.get_all_items()
        # then
        assert result == items


class TestSaveItem:
    def test_returns_saved_item(self, repo):
        # given
        item = item_factory()
        # when
        result = repo.save_item(item)
        # then
        assert result == item
