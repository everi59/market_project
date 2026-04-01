from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.api.v1.dependencies import get_category_repo
from app.core.dto.category_dto import CategoryDetailDTO, CategoryTreeResponseDTO
from app.core.dto.filter_dto import FiltersResponseDTO
from app.core.repositories.category_repository import CategoryRepository


router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("", response_model=CategoryTreeResponseDTO)
async def get_category_tree(
    repo: CategoryRepository = Depends(get_category_repo),
) -> CategoryTreeResponseDTO:
    items = await repo.get_tree()
    return CategoryTreeResponseDTO(items=items)


@router.get("/{id}", response_model=CategoryDetailDTO)
async def get_category(
    id: UUID,
    include_product_count: bool = False,
    repo: CategoryRepository = Depends(get_category_repo),
) -> CategoryDetailDTO:
    category = await repo.get_by_id(id, include_product_count=include_product_count)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.get("/{id}/filters", response_model=FiltersResponseDTO)
async def get_category_filters(
    id: UUID,
    repo: CategoryRepository = Depends(get_category_repo),
) -> FiltersResponseDTO:
    if not await repo.exists(id):
        raise HTTPException(status_code=404, detail="Category not found")
    items = await repo.get_filters(id)
    return FiltersResponseDTO(items=items)

