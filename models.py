from typing import Optional

from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # unique=True: kahta samannimistä kategoriaa ei ole järkeä olla
    name: Mapped[str] = mapped_column(Text, nullable=False, unique=True)


class Item(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Viiteavain — tämä on oikeasti tietokannassa sarakkeena
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=False)

    # relationship EI ole sarake tietokannassa
    category: Mapped['Category'] = relationship('Category', back_populates='items')