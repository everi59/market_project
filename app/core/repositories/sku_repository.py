from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.core.repositories.category_repository import CategoryRepository
from app.core.repositories.product_repository import ProductRepository
from app.core.dto.breadcrumb_dto import (
    BreadcrumbItemDTO,
    BreadcrumbMetaDTO,
    BreadcrumbResponseDTO,
)


class BreadcrumbRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.category_repo = CategoryRepository(session)
        self.product_repo = ProductRepository(session)

    async def build_for_category(
            self,
            category_id: UUID
    ) -> List[BreadcrumbItemDTO]:
        """Построить breadcrumb для категории"""
        path = await self.category_repo.get_path_to_root(category_id)

        if not path:
            return []

        breadcrumbs = []
        for idx, category in enumerate(path):
            # Строим URL из slug'ов всех предков
            url_parts = [cat.slug for cat in path[:idx + 1]]
            url = "/catalog/" + "/".join(url_parts)

            breadcrumbs.append(
                BreadcrumbItemDTO(
                    id=category.id,
                    slug=category.slug,
                    name=category.name,
                    url=url,
                    level=idx,
                    is_current=(idx == len(path) - 1),
                )
            )

        return breadcrumbs

    async def build_for_product(
            self,
            product_id: UUID
    ) -> List[BreadcrumbItemDTO]:
        """Построить breadcrumb для товара (через его категорию)"""
        product = await self.product_repo.get_by_id(product_id)

        if not product:
            return []

        # Получаем category_id из product (нужно добавить в Product DTO)
        # Для этого нужен отдельный запрос
        from app.infrastructure.database.models.product import Product
        from sqlalchemy import select

        result = await self.session.execute(
            select(Product.category_id).where(Product.id == product_id)
        )
        row = result.one_or_none()

        if not row or not row[0]:
            return []

        category_id = row[0]
        return await self.build_for_category(category_id)

    async def build(
            self,
            category_id: Optional[UUID] = None,
            product_id: Optional[UUID] = None,
    ) -> Optional[BreadcrumbResponseDTO]:
        """Универсальный метод построения breadcrumb"""
        if category_id:
            breadcrumbs = await self.build_for_category(category_id)
            resolved_via = "category_id"
        elif product_id:
            breadcrumbs = await self.build_for_product(product_id)
            resolved_via = "product_id"
        else:
            return None

        if not breadcrumbs:
            return None

        return BreadcrumbResponseDTO(
            data=breadcrumbs,
            meta=BreadcrumbMetaDTO(
                resolved_via=resolved_via,
                category_id=category_id,
                product_id=product_id,
            )
        )
