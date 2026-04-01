from pydantic import BaseModel, Field
from typing import List, Literal, Optional
from uuid import UUID


class BreadcrumbItemDTO(BaseModel):
    id: UUID
    slug: str
    name: str
    url: str
    level: int
    is_current: bool = False

    class Config:
        from_attributes = True


class BreadcrumbMetaDTO(BaseModel):
    resolved_via: Literal["category_id", "product_id"]
    category_id: Optional[UUID] = None
    product_id: Optional[UUID] = None

    class Config:
        from_attributes = True


class BreadcrumbResponseDTO(BaseModel):
    data: List[BreadcrumbItemDTO]
    meta: BreadcrumbMetaDTO
