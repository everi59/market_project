from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from enum import Enum


class ProductStatusEnum(str, Enum):
    CREATED = "CREATED"
    ON_MODERATED = "ON_MODERATED"
    MODERATED = "MODERATED"
    BLOCKED = "BLOCKED"


class ImageDTO(BaseModel):
    url: str = Field(..., format="uri")
    order: int

    class Config:
        from_attributes = True


class CharacteristicDTO(BaseModel):
    name: str
    value: str

    class Config:
        from_attributes = True


class SkuShortDTO(BaseModel):
    name: str
    price: float
    image: ImageDTO

    class Config:
        from_attributes = True


class SkuDTO(BaseModel):
    id: UUID
    name: str
    price: float
    quantity: int
    characteristics: List[CharacteristicDTO]
    images: List[ImageDTO] = []

    class Config:
        from_attributes = True


class ProductShortDTO(BaseModel):
    id: UUID
    title: str
    image: str = Field(..., format="uri")
    price: float
    in_stock: bool
    is_in_cart: bool

    class Config:
        from_attributes = True


class ProductShortListResponseDTO(BaseModel):
    total_count: int
    limit: int
    offset: int
    items: List[ProductShortDTO]


class ProductDTO(BaseModel):
    id: UUID
    slug: str
    title: str
    description: str
    images: List[ImageDTO]
    status: ProductStatusEnum
    characteristics: List[CharacteristicDTO]
    skus: List[SkuDTO]

    class Config:
        from_attributes = True

