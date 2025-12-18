CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    role VARCHAR(50) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    login VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    article VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    unit VARCHAR(20) NOT NULL,
    price int NOT NULL,
    provider VARCHAR(100) NOT NULL,
    manufacturer VARCHAR(100) NOT NULL,
    category VARCHAR(100) NOT NULL,
    discount smallint DEFAULT 0,
    quantity int NOT NULL,
    description TEXT,
    image_url VARCHAR(255)
);

CREATE TABLE pickup_points (
    id SERIAL PRIMARY KEY,
    address VARCHAR(255) NOT NULL
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    order_number int NOT NULL UNIQUE,
    order_date TIMESTAMP NOT NULL,
    delivery_date TIMESTAMP NOT NULL,
    pickup_point_id int NOT NULL,
    user_id int NOT NULL,
    receipt_code int NOT NULL,
    status VARCHAR(50) NOT NULL,

    FOREIGN KEY (pickup_point_id) REFERENCES pickup_points(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);



CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id)
);
