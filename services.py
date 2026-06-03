from sqlalchemy.orm import Session
from models import Users, Products, ShopList, ListItems

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, login: str, password: str, name: str) -> Users:
        user = Users(login=login, password=password, name=name)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_login(self, login: str) -> Users | None:
        return self.db.query(Users).filter(Users.login == login).first()


class ProductService:
    def __init__(self, db: Session):
        self.db = db

    def create_product(self, user_id: int, name: str, count: float = 0.0) -> Products:
        product = Products(user_id=user_id, name=name, count=count)
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def get_products_by_user(self, user_id: int) -> list[Products]:
        return self.db.query(Products).filter(Products.user_id == user_id).all()


class ShopListService:
    def __init__(self, db: Session):
        self.db = db

    def create_list(self, user_id: int) -> ShopList:
        shop_list = ShopList(user_id=user_id)
        self.db.add(shop_list)
        self.db.commit()
        self.db.refresh(shop_list)
        return shop_list

    def add_item(self, list_id: int, product_id: int, count: float = 1.0) -> ListItems:
        item = ListItems(list_id=list_id, product_id=product_id, count=count)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item