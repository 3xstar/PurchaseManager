-- 1. Пользователи
CREATE TABLE Users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    login VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL
);

-- 2. Роли
CREATE TABLE Roles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(50) NOT NULL UNIQUE
);

-- 3. Связь пользователей и ролей
CREATE TABLE User_Roles (
    user_id INT NOT NULL,
    role_id INT NOT NULL,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES Roles(id) ON DELETE CASCADE
);

-- 4. Категории
CREATE TABLE Categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100) NOT NULL UNIQUE
);

-- 5. Единицы измерения
CREATE TABLE Units (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(50) NOT NULL UNIQUE
);

-- 6. Продукты
CREATE TABLE Products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    name VARCHAR(150) NOT NULL,
    category_id INT,
    unit_id INT,
    count DECIMAL(10,2) DEFAULT 0,
    add_date DATE DEFAULT (CURDATE()),
    expire_date DATE,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES Categories(id) ON DELETE SET NULL,
    FOREIGN KEY (unit_id) REFERENCES Units(id) ON DELETE SET NULL,
    CHECK (count >= 0),
    CHECK (expire_date IS NULL OR expire_date > add_date)
);

-- 7. Списки покупок
CREATE TABLE Shop_List (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    create_date DATE DEFAULT (CURDATE()),
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
);

-- 8. Элементы списков
CREATE TABLE List_Items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    list_id INT NOT NULL,
    product_id INT NOT NULL,
    count DECIMAL(10,2) DEFAULT 1,
    FOREIGN KEY (list_id) REFERENCES Shop_List(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Products(id) ON DELETE CASCADE,
    CHECK (count > 0),
    UNIQUE (list_id, product_id)
);

-- Индексы для быстрого поиска по связям
CREATE INDEX idx_products_user ON Products(user_id);
CREATE INDEX idx_products_expire ON Products(expire_date);
CREATE INDEX idx_shop_list_user ON Shop_List(user_id);
CREATE INDEX idx_list_items_list ON List_Items(list_id);
CREATE INDEX idx_list_items_product ON List_Items(product_id);