from typing import Optional, List, Tuple, Dict, Any
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.sql import Select
from uuid import UUID
from app.core.repositories.base import SqlAlchemyRepository
from app.infrastructure.database.models.product import Product, ProductStatus
from app.infrastructure.database.models.sku import Sku


class ProductRepository(SqlAlchemyRepository[Product]):
    """Репозиторий для работы с товарами"""

    def __init__(self, session):
        super().__init__(session, Product)

    async def get_products(
            self,
            limit: int = 10,
            offset: int = 0,
            category_id: Optional[UUID] = None,
            sort: Optional[str] = None,
            search: Optional[str] = None,
            filters: Optional[Dict[str, Any]] = None,
    ) -> Tuple[List[Product], int]:
        """Получить список товаров с фильтрами и пагинацией"""
        # Базовый запрос
        query = select(Product).where(Product.status == ProductStatus.MODERATED)

        # Фильтр по категории
        if category_id:
            query = query.where(Product.category_id == category_id)

        # Поиск по названию/описанию
        if search and len(search) >= 3:
            query = query.where(
                or_(
                    Product.title.ilike(f"%{search}%"),
                    Product.description.ilike(f"%{search}%"),
                )
            )

        # Сортировка
        query = self._apply_sort(query, sort)

        # Получаем общее количество
        count_query = select(func.count()).select_from(Product).where(
            Product.status == ProductStatus.MODERATED
        )
        if category_id:
            count_query = count_query.where(Product.category_id == category_id)
        if search:
            count_query = count_query.where(
                or_(
                    Product.title.ilike(f"%{search}%"),
                    Product.description.ilike(f"%{search}%"),
                )
            )

        total_result = await self.session.execute(count_query)
        total = total_result.scalar_one() or 0

        # Пагинация
        query = query.offset(offset).limit(limit)

        # Загружаем связанные данные
        query = query.options(
            joinedload(Product.category),
            joinedload(Product.images),
            selectinload(Product.skus),
        )

        result = await self.session.execute(query)
        products = result.scalars().unique().all()

        return products, total

    def _apply_sort(self, query: Select, sort: Optional[str]) -> Select:
        """Применить сортировку к запросу"""
        if sort == "price_asc":
            query = query.join(Sku).order_by(Sku.price.asc())
        elif sort == "price_desc":
            query = query.join(Sku).order_by(Sku.price.desc())
        elif sort == "date_desc":
            query = query.order_by(Product.created_at.desc())
        elif sort == "date_asc":
            query = query.order_by(Product.created_at.asc())
        else:
            query = query.order_by(Product.created_at.desc())
        return query

    async def get_by_slug(self, slug: str) -> Optional[Product]:
        """Получить товар по slug"""
        result = await self.session.execute(
            select(Product)
            .where(Product.slug == slug)
            .options(
                joinedload(Product.category),
                joinedload(Product.images),
                joinedload(Product.characteristics),
                selectinload(Product.skus).joinedload(Sku.characteristics),
                selectinload(Product.skus).joinedload(Sku.images),
            )
        )
        return result.scalar_one_or_none()

    async def get_similar(
            self,
            product_id: UUID,
            category_id: UUID,
            limit: int = 8
    ) -> List[Product]:
        """Получить похожие товары из той же категории"""
        result = await self.session.execute(
            select(Product)
            .where(
                Product.category_id == category_id,
                Product.id != product_id,
                Product.status == ProductStatus.MODERATED,
            )
            .options(joinedload(Product.images))
            .limit(limit)
        )
        return result.scalars().all()

    async def get_min_max_price(self, category_id: Optional[UUID] = None) -> Tuple[float, float]:
        """Получить минимальную и максимальную цену"""
        query = select(func.min(Sku.price), func.max(Sku.price)).select_from(Sku)
        query = query.join(Product, Sku.product_id == Product.id)
        query = query.where(Product.status == ProductStatus.MODERATED)

        if category_id:
            query = query.where(Product.category_id == category_id)

        result = await self.session.execute(query)
        row = result.one()
        return (row[0] or 0, row[1] or 0)
