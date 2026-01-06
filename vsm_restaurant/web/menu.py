from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select

from vsm_restaurant.db.ingredients import Ingredient
from vsm_restaurant.db.menu import MenuItem
from vsm_restaurant.dependencies import SessionDep, require_admin_token


public_router = APIRouter(tags=["menu"])
admin_router = APIRouter(
    prefix="/admin/menu",
    tags=["admin-menu"],
    dependencies=[Depends(require_admin_token)],
)


def _is_orderable(session, item: MenuItem) -> bool:
    if not item.is_available:
        return False
    if not item.composition:
        return True

    # composition is list of {ingredient_id, quantity}
    for row in item.composition:
        try:
            ing_id = int(row.get("ingredient_id"))
            qty = int(row.get("quantity"))
        except Exception:
            return False

        ing = session.get(Ingredient, ing_id)
        if ing is None:
            return False
        if ing.stock < qty:
            return False
    return True


@public_router.get("/menu")
async def get_public_menu(session: SessionDep):
    items = list(session.exec(select(MenuItem).order_by(MenuItem.id)))
    return [i for i in items if _is_orderable(session, i)]


@admin_router.get("")
async def list_menu_admin(session: SessionDep):
    return list(session.exec(select(MenuItem).order_by(MenuItem.id)))


@admin_router.post("", status_code=status.HTTP_201_CREATED)
async def create_menu_item(session: SessionDep, model: MenuItem):
    model.id = None
    session.add(model)
    session.commit()
    session.refresh(model)
    return model


@admin_router.patch("/{menu_id}")
async def update_menu_item(session: SessionDep, menu_id: int, patch: dict[str, Any]):
    item = session.get(MenuItem, menu_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")

    for k, v in patch.items():
        if k in {"id"}:
            continue
        if hasattr(item, k):
            setattr(item, k, v)

    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@admin_router.delete("/{menu_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_menu_item(session: SessionDep, menu_id: int):
    item = session.get(MenuItem, menu_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    session.delete(item)
    session.commit()
    return None
