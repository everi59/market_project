from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from app.core.dto.product_dto import ImageDTO, CharacteristicDTO


class SkuDTO(BaseModel):
    id: UUID
    name: str
    price: float
    quantity: int
    characteristics: List[CharacteristicDTO]
    images: List[ImageDTO] = []

    class Config:
        from_attributes = True


class SkuShortDTO(BaseModel):
    name: str
    price: float
    image: ImageDTO


class SkusShortDTO(BaseModel):
    items: List[SkuShortDTO]
    