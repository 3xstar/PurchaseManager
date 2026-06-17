from sqlalchemy.orm import Session
from modules_project.models.models import Users, Products, ShopList, ListItems, Categories
from typing import Optional

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, login: str, password: str, name: str) -> Users:
        user = Users(login=login, password=password, name=name)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_login(self, login: str) -> Optional[Users]:
        return self.db.query(Users).filter(Users.login == login).first()


class ProductService:
    def __init__(self, db: Session):
        self.db = db

    def create_product(self, user_id: int, name: str, count: float = 0.0, category_title: str = None, expire_date_str: str = None) -> Products:
        from datetime import datetime
        
        category_id = None
        if category_title:
            cat = self.db.query(Categories).filter(Categories.title == category_title).first()
            if not cat:
                cat = Categories(title=category_title)
                self.db.add(cat)
                self.db.flush() 
            category_id = cat.id

        expire_date_obj = None
        if expire_date_str:
            try:
                expire_date_obj = datetime.strptime(expire_date_str, "%d.%m.%Y").date()
            except ValueError:
                pass

        product = Products(
            user_id=user_id, 
            name=name, 
            count=count, 
            category_id=category_id,
            expire_date=expire_date_obj
        )
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def get_products_by_user(self, user_id: int) -> list[Products]:
        return self.db.query(Products).filter(Products.user_id == user_id).all()
        
    def update_product(self, product_id: int, name: str, count: float, category_title: str = None, expire_date_str: str = None) -> bool:
        from datetime import datetime
        
        product = self.db.query(Products).filter(Products.id == product_id).first()
        if not product:
            return False

        product.name = name
        product.count = count
        
        if category_title:
            cat = self.db.query(Categories).filter(Categories.title == category_title).first()
            if not cat:
                cat = Categories(title=category_title)
                self.db.add(cat)
                self.db.flush()
            product.category_id = cat.id
        else:
            product.category_id = None

        if expire_date_str:
            try:
                product.expire_date = datetime.strptime(expire_date_str, "%d.%m.%Y").date()
            except ValueError:
                product.expire_date = None
        else:
            product.expire_date = None

        self.db.commit()
        return True

    def delete_product(self, product_id: int) -> bool:
        product = self.db.query(Products).filter(Products.id == product_id).first()
        if product:
            self.db.delete(product)
            self.db.commit()
            return True
        return False

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