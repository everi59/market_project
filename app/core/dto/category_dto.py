from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime


class CategoryParentDTO(BaseModel):
    id: UUID
    name: str
    slug: str

    class Config:
        from_attributes = True


class CategorySeoDTO(BaseModel):
    title: str
    description: str
    keywords: Optional[List[str]] = []

    class Config:
        from_attributes = True


class CategoryMetaTagsDTO(BaseModel):
    og_title: Optional[str] = None
    og_description: Optional[str] = None
    og_image: Optional[str] = None
    twitter_card: Optional[str] = None

    class Config:
        from_attributes = True


class CategoryNodeDTO(BaseModel):
    id: UUID
    name: str
    parent_id: Optional[UUID] = None
    children: List["CategoryNodeDTO"] = []

    class Config:
        from_attributes = True


class CategoryTreeResponseDTO(BaseModel):
    items: List[CategoryNodeDTO]


class CategoryDetailDTO(BaseModel):
    id: UUID
    name: str
    slug: str
    description: Optional[str] = None
    parent: Optional[CategoryParentDTO] = None
    product_count: Optional[int] = None
    seo: CategorySeoDTO
    meta_tags: CategoryMetaTagsDTO
    image_url: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True