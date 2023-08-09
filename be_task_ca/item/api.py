from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..common import get_db
from .repository import SqlItemRepository
from .schema import CreateItemRequest, CreateItemResponse
from .usecases import ItemAlreadyExistsError, create_item, get_all

item_router = APIRouter(
    prefix="/items",
    tags=["item"],
)


@item_router.post("/")
async def post_item(
    item: CreateItemRequest, db: Session = Depends(get_db)
) -> CreateItemResponse:
    try:
        return create_item(item, SqlItemRepository(db))
    except ItemAlreadyExistsError as err:
        raise HTTPException(status_code=409, detail=str(err))


@item_router.get("/")
async def get_items(db: Session = Depends(get_db)):
    return get_all(SqlItemRepository(db))
