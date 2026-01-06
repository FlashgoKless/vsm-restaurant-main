from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select

from vsm_restaurant.db.ingredients import Ingredient
from vsm_restaurant.dependencies import SessionDep, require_admin_token


router = APIRouter(
    prefix="/admin/ingredients",
    tags=["admin-ingredients"],
    dependencies=[Depends(require_admin_token)],
)


@router.get("")
async def list_ingredients(session: SessionDep):
    return list(session.exec(select(Ingredient).order_by(Ingredient.id)))


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_ingredient(session: SessionDep, model: Ingredient):
    model.id = None
    if model.stock is None:
        model.stock = 0
    if model.stock < 0:
        raise HTTPException(status_code=400, detail="stock must be >= 0")
    session.add(model)
    session.commit()
    session.refresh(model)
    return model


@router.patch("/{ingredient_id}")
async def update_ingredient(session: SessionDep, ingredient_id: int, patch: dict[str, Any]):
    ing = session.get(Ingredient, ingredient_id)
    if ing is None:
        raise HTTPException(status_code=404, detail="Ingredient not found")

    for k, v in patch.items():
        if k in {"id"}:
            continue
        if k == "stock" and v is not None and int(v) < 0:
            raise HTTPException(status_code=400, detail="stock must be >= 0")
        if hasattr(ing, k):
            setattr(ing, k, v)

    session.add(ing)
    session.commit()
    session.refresh(ing)
    return ing


@router.post("/{ingredient_id}/adjust")
async def adjust_stock(session: SessionDep, ingredient_id: int, body: dict[str, Any]):
    """Adjust ingredient stock by delta (positive = add, negative = subtract)."""
    ing = session.get(Ingredient, ingredient_id)
    if ing is None:
        raise HTTPException(status_code=404, detail="Ingredient not found")

    if "delta" not in body:
        raise HTTPException(status_code=400, detail="Missing delta")

    try:
        delta = int(body["delta"])
    except Exception:
        raise HTTPException(status_code=400, detail="delta must be int")

    new_stock = int(ing.stock) + delta
    if new_stock < 0:
        raise HTTPException(status_code=400, detail="Not enough stock")

    ing.stock = new_stock
    session.add(ing)
    session.commit()
    session.refresh(ing)
    return ing


@router.delete("/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ingredient(session: SessionDep, ingredient_id: int):
    ing = session.get(Ingredient, ingredient_id)
    if ing is None:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    session.delete(ing)
    session.commit()
    return None
