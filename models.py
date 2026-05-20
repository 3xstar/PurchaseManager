from typing import Optional
import datetime
import decimal

from sqlalchemy import CheckConstraint, Column, DECIMAL, Date, ForeignKeyConstraint, Index, String, Table, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Categories(Base):
    __tablename__ = 'categories'
    __table_args__ = (
        Index('title', 'title', unique=True),
    )

    id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)

    products: Mapped[list['Products']] = relationship('Products', back_populates='category')


class Roles(Base):
    __tablename__ = 'roles'
    __table_args__ = (
        Index('title', 'title', unique=True),
    )

    id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)

    user: Mapped[list['Users']] = relationship('Users', secondary='user_roles', back_populates='role')


class Units(Base):
    __tablename__ = 'units'
    __table_args__ = (
        Index('title', 'title', unique=True),
    )

    id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)

    products: Mapped[list['Products']] = relationship('Products', back_populates='unit')


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        Index('login', 'login', unique=True),
    )

    id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    login: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    role: Mapped[list['Roles']] = relationship('Roles', secondary='user_roles', back_populates='user')
    products: Mapped[list['Products']] = relationship('Products', back_populates='user')
    shop_list: Mapped[list['ShopList']] = relationship('ShopList', back_populates='user')


class Products(Base):
    __tablename__ = 'products'
    __table_args__ = (
        CheckConstraint('`count` >= 0', name='CONSTRAINT_1'),
        CheckConstraint('`expire_date` is null or `expire_date` > `add_date`', name='CONSTRAINT_2'),
        ForeignKeyConstraint(['category_id'], ['categories.id'], ondelete='SET NULL', name='products_ibfk_2'),
        ForeignKeyConstraint(['unit_id'], ['units.id'], ondelete='SET NULL', name='products_ibfk_3'),
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='products_ibfk_1'),
        Index('category_id', 'category_id'),
        Index('idx_products_expire', 'expire_date'),
        Index('idx_products_user', 'user_id'),
        Index('unit_id', 'unit_id')
    )

    id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    user_id: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    category_id: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    unit_id: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    count: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 2), server_default=text('0.00'))
    add_date: Mapped[Optional[datetime.date]] = mapped_column(Date, server_default=text('curdate()'))
    expire_date: Mapped[Optional[datetime.date]] = mapped_column(Date)

    category: Mapped[Optional['Categories']] = relationship('Categories', back_populates='products')
    unit: Mapped[Optional['Units']] = relationship('Units', back_populates='products')
    user: Mapped['Users'] = relationship('Users', back_populates='products')
    list_items: Mapped[list['ListItems']] = relationship('ListItems', back_populates='product')


class ShopList(Base):
    __tablename__ = 'shop_list'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='shop_list_ibfk_1'),
        Index('idx_shop_list_user', 'user_id')
    )

    id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    user_id: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    create_date: Mapped[Optional[datetime.date]] = mapped_column(Date, server_default=text('curdate()'))

    user: Mapped['Users'] = relationship('Users', back_populates='shop_list')
    list_items: Mapped[list['ListItems']] = relationship('ListItems', back_populates='list')


t_user_roles = Table(
    'user_roles', Base.metadata,
    Column('user_id', INTEGER(11), primary_key=True),
    Column('role_id', INTEGER(11), primary_key=True),
    ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE', name='user_roles_ibfk_2'),
    ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='user_roles_ibfk_1'),
    Index('role_id', 'role_id')
)


class ListItems(Base):
    __tablename__ = 'list_items'
    __table_args__ = (
        CheckConstraint('`count` > 0', name='CONSTRAINT_1'),
        ForeignKeyConstraint(['list_id'], ['shop_list.id'], ondelete='CASCADE', name='list_items_ibfk_1'),
        ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='CASCADE', name='list_items_ibfk_2'),
        Index('idx_list_items_list', 'list_id'),
        Index('idx_list_items_product', 'product_id'),
        Index('list_id', 'list_id', 'product_id', unique=True)
    )

    id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    list_id: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    product_id: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    count: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 2), server_default=text('1.00'))

    list: Mapped['ShopList'] = relationship('ShopList', back_populates='list_items')
    product: Mapped['Products'] = relationship('Products', back_populates='list_items')
