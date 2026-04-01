from __future__ import annotations

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.api.v1.dependencies import get_breadcrumb_repo
from app.core.dto.breadcrumb_dto import BreadcrumbResponseDTO
from app.core.dto.error_dto import ErrorResponseDTO
from app.core.repositories.sku_repository import BreadcrumbRepository


router = APIRouter(prefix="/breadcrumbs", tags=["Breadcrumbs"])


@router.get("", response_model=BreadcrumbResponseDTO)
async def build_breadcrumbs(
    category_id: Optional[UUID] = None,
    product_id: Optional[UUID] = None,
    lang: str = "ru",
    repo: BreadcrumbRepository = Depends(get_breadcrumb_repo),
):
    if not category_id and not product_id:
        err = ErrorResponseDTO(
            error="missing_param",
            message="category_id or product_id must be provided",
        )
        return JSONResponse(status_code=400, content=err.model_dump())

    if category_id and product_id:
        err = ErrorResponseDTO(
            error="ambiguous_param",
            message="only one of category_id or product_id must be provided",
        )
        return JSONResponse(status_code=400, content=err.model_dump())

    result = await repo.build(category_id=category_id, product_id=product_id)
    if not result:
        err = ErrorResponseDTO(
            error="not_found",
            message="category not found" if category_id else "product not found",
        )
        return JSONResponse(status_code=404, content=err.model_dump())

    return JSONResponse(
        status_code=200,
        headers={"cache-control": "public, max-age=300"},
        content=result.model_dump(),
    )

