from __future__ import annotations

from typing import Any, Dict, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.api.v1.dependencies import get_category_repo, get_filters_from_query
from app.core.dto.filter_dto import FacetDTO, FacetsResponseDTO
from app.core.repositories.category_repository import CategoryRepository


router = APIRouter(prefix="/catalog", tags=["Catalog"])


@router.get("/facets", response_model=FacetsResponseDTO)
async def get_facets(
    category_id: UUID,
    filters: Optional[Dict[str, Any]] = Depends(get_filters_from_query),
    repo: CategoryRepository = Depends(get_category_repo),
) -> FacetsResponseDTO:
    if not await repo.exists(category_id):
        raise HTTPException(status_code=404, detail="Category not found")

    facets_raw = await repo.get_facets(category_id, filters=filters)
    facets = [FacetDTO(**f) for f in facets_raw]
    return FacetsResponseDTO(category_id=category_id, facets=facets)

