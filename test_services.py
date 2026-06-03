from services import UserService, ProductService, ShopListService


def test_user_service(db_session):
    service = UserService(db_session)
    user = service.create_user(login="testuser", password="secure_pwd", name="Test User")

    assert user.id is not None
    assert user.login == "testuser"

    fetched_user = service.get_user_by_login("testuser")
    assert fetched_user is not None
    assert fetched_user.name == "Test User"


def test_product_service(db_session):
    user_service = UserService(db_session)
    user = user_service.create_user(login="produser", password="pwd", name="Prod User")

    product_service = ProductService(db_session)
    product = product_service.create_product(user_id=user.id, name="Milk", count=2.5)

    assert product.id is not None
    assert product.name == "Milk"
    assert product.count == 2.5

    products = product_service.get_products_by_user(user.id)
    assert len(products) == 1
    assert products[0].name == "Milk"


def test_shop_list_service(db_session):
    user_service = UserService(db_session)
    user = user_service.create_user(login="listuser", password="pwd", name="List User")

    product_service = ProductService(db_session)
    product = product_service.create_product(user_id=user.id, name="Bread", count=1.0)

    list_service = ShopListService(db_session)
    shop_list = list_service.create_list(user_id=user.id)

    item = list_service.add_item(list_id=shop_list.id, product_id=product.id, count=1.0)

    assert item.id is not None
    assert item.count == 1.0
    assert item.list_id == shop_list.id
    assert item.product_id == product.id