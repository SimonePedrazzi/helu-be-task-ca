import json
from uuid import uuid4
from fastapi.testclient import TestClient
import pytest
from fastapi import FastAPI, Request
from be_task_ca.item.api import item_router, get_db
from be_task_ca.item.schema import CreateItemResponse

from typing import cast
from sqlalchemy.orm import Session

from be_task_ca.item.usecases import ItemAlreadyExistsError


def item_response_factory(**kwargs) -> CreateItemResponse:
    defaults = {
        "id": uuid4(),
        "name": "abc",
        "description": "lorem ipsum",
        "price": 10,
        "quantity": 3,
    }
    return CreateItemResponse(**(defaults | kwargs))


@pytest.fixture
def app(mocker):
    async def override_dependency(request: Request):
        return cast(Session, mocker.Mock())

    app_ = FastAPI()
    app_.include_router(item_router)

    app_.dependency_overrides[get_db] = override_dependency

    return app_


@pytest.fixture
def client(app):
    return TestClient(app)


def test_returns_200(mocker, client):
    # given
    data = {"name": "some-item", "price": 25, "quantity": 1}
    item_response = item_response_factory(**data)
    mocker.patch("be_task_ca.item.api.create_item", return_value=item_response)
    # when
    response = client.post("/items/", json=data)
    # then
    assert response.status_code == 200
    assert response.json() == json.loads(item_response.model_dump_json())


def test_returns_409(mocker, client):
    # given
    data = {"name": "some-item", "price": 25, "quantity": 1}
    err = ItemAlreadyExistsError("some error message")
    mocker.patch("be_task_ca.item.api.create_item", side_effect=err)
    # when
    response = client.post("/items/", json=data)
    # then
    assert response.status_code == 409
