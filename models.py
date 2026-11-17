
from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # unique=True: kahta samannimistä kategoriaa ei ole järkeä olla
    name: Mapped[str] = mapped_column(Text, nullable=False, unique=True)

    items: Mapped[list['Item']] = relationship('Item', back_populates='category')


class Item(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Viiteavain — tämä on oikeasti tietokannassa sarakkeena
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=False)

    # relationship EI ole sarake tietokannassa
    category: Mapped['Category'] = relationship('Category', back_populates='items')

    copies: Mapped[list['ItemCopy']] = relationship('ItemCopy', back_populates='item')



class ItemCopy(Base):
    __tablename__ = 'item_copies'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Inventaariokoodi, esim. "CAM-001"
    inventory_code: Mapped[str] = mapped_column(Text, nullable=False, unique=True)

    item_id: Mapped[int] = mapped_column(ForeignKey('items.id'), nullable=False)
    item: Mapped['Item'] = relationship('Item', back_populates='copies')