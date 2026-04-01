from __future__ import annotations

# Backwards-compat: the legacy `Characteristic` model used to live here.
# The current schema uses `ProductCharacteristic` and `SkuCharacteristic`.
from app.infrastructure.database.models.product import ProductCharacteristic as Characteristic  # noqa: F401

