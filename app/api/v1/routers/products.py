from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.api.v1.dependencies import get_category_repo, get_filters_from_query, get_product_repo
from app.core.dto.product_dto import (
    ProductDTO,
    ProductShortListResponseDTO,
    SkuDTO,
    SkuShortDTO,
)
from app.core.repositories.product_repository import ProductRepository
from app.core.repositories.category_repository import CategoryRepository


router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=ProductShortListResponseDTO)
async def list_products(
    limit: int = 10,
    offset: int = 0,
    category_id: Optional[UUID] = None,
    sort: Optional[str] = None,
    search: Optional[str] = None,
    filters: Optional[Dict[str, Any]] = Depends(get_filters_from_query),
    repo: ProductRepository = Depends(get_product_repo),
) -> ProductShortListResponseDTO:
    items, total = await repo.get_products(
        limit=limit,
        offset=offset,
        category_id=category_id,
        sort=sort,
        search=search,
        filters=filters,
    )
    return ProductShortListResponseDTO(
        total_count=total,
        limit=limit,
        offset=offset,
        items=items,
    )


@router.get("/{id}", response_model=ProductDTO)
async def get_product(
    id: UUID,
    repo: ProductRepository = Depends(get_product_repo),
) -> ProductDTO:
    product = await repo.get_by_id(id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("/{id}/similar", response_model=ProductShortListResponseDTO)
async def get_similar_products(
    id: UUID,
    category: UUID,
    limit: int = 8,
    offset: int = 0,
    repo: ProductRepository = Depends(get_product_repo),
    category_repo: CategoryRepository = Depends(get_category_repo),
) -> ProductShortListResponseDTO:
    if not await repo.exists(id):
        raise HTTPException(status_code=404, detail="Product not found")
    if not await category_repo.exists(category):
        raise HTTPException(status_code=400, detail="Nonexistent category id")

    items, total = await repo.get_similar_products(
        product_id=id,
        category_id=category,
        limit=limit,
        offset=offset,
    )
    return ProductShortListResponseDTO(
        total_count=total,
        limit=limit,
        offset=offset,
        items=items,
    )


@router.get("/{product_id}/skus", response_model=List[SkuShortDTO])
async def list_product_skus(
    product_id: UUID,
    repo: ProductRepository = Depends(get_product_repo),
) -> List[SkuShortDTO]:
    if not await repo.exists(product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    return await repo.get_skus(product_id)


@router.get("/{product_id}/skus/{sku_id}", response_model=SkuDTO)
async def get_product_sku(
    product_id: UUID,
    sku_id: UUID,
    repo: ProductRepository = Depends(get_product_repo),
) -> SkuDTO:
    if not await repo.exists(product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    sku = await repo.get_sku(product_id=product_id, sku_id=sku_id)
    if not sku:
        raise HTTPException(status_code=404, detail="SKU not found")
    return sku
