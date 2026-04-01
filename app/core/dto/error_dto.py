from __future__ import annotations

from pydantic import BaseModel


class ErrorResponseDTO(BaseModel):
    message: str
    error: str | None = None

