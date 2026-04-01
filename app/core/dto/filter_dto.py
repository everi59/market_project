from pydantic import BaseModel, Field
from typing import List, Optional, Union, Literal
from uuid import UUID


class FilterDTO(BaseModel):
    slug: str
    name: str
    type: Literal["list", "range", "switch"]
    value: Optional[List[Union[str, int, float]]] = None
    min: Optional[float] = None
    max: Optional[float] = None

    class Config:
        from_attributes = True


class FiltersResponseDTO(BaseModel):
    items: List[FilterDTO]


class FacetValueDTO(BaseModel):
    value: str
    count: int

    class Config:
        from_attributes = True


class FacetDTO(BaseModel):
    name: str
    values: List[FacetValueDTO]

    class Config:
        from_attributes = True


class FacetsResponseDTO(BaseModel):
    category_id: UUID
    facets: List[FacetDTO]

