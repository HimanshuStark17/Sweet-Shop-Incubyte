-- Drop existing tables
DROP TABLE IF EXISTS purchase_items CASCADE;
DROP TABLE IF EXISTS purchases CASCADE;
DROP TABLE IF EXISTS suppliers CASCADE;
DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Create users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'customer',
    full_name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_role CHECK (role IN ('admin', 'customer'))
);

-- Create products table
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INTEGER NOT NULL DEFAULT 0,
    unit VARCHAR(20) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_price CHECK (price >= 0),
    CONSTRAINT chk_stock CHECK (stock_quantity >= 0)
);

-- Create customers table
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    phone VARCHAR(15) UNIQUE NOT NULL,
    email VARCHAR(100),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create orders table
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    user_id INTEGER REFERENCES users(user_id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL,
    payment_method VARCHAR(20),
    status VARCHAR(20) DEFAULT 'pending',
    CONSTRAINT chk_status CHECK (status IN ('pending', 'completed', 'cancelled')),
    CONSTRAINT chk_payment CHECK (payment_method IN ('cash', 'card', 'upi'))
);

-- Create order_items table
CREATE TABLE order_items (
    item_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(product_id),
    quantity DECIMAL(10, 2) NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    CONSTRAINT chk_quantity CHECK (quantity > 0),
    CONSTRAINT chk_unit_price CHECK (unit_price >= 0)
);

-- Create suppliers table
CREATE TABLE suppliers (
    supplier_id SERIAL PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL,
    contact_person VARCHAR(100),
    phone VARCHAR(15),
    email VARCHAR(100),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create purchases table
CREATE TABLE purchases (
    purchase_id SERIAL PRIMARY KEY,
    supplier_id INTEGER REFERENCES suppliers(supplier_id),
    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'completed',
    CONSTRAINT chk_purchase_status CHECK (status IN ('pending', 'completed', 'cancelled'))
);

-- Create purchase_items table
CREATE TABLE purchase_items (
    item_id SERIAL PRIMARY KEY,
    purchase_id INTEGER REFERENCES purchases(purchase_id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(product_id),
    quantity DECIMAL(10, 2) NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL
);

-- Create indexes
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_product ON order_items(product_id);

-- Insert admin user (password: admin123)
INSERT INTO users (username, password_hash, role, full_name, email, phone) 
VALUES ('admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin', 'Admin User', 'admin@sweetshop.com', '9999999999');

-- Insert customer user (password: customer123)
INSERT INTO users (username, password_hash, role, full_name, email, phone) 
VALUES ('customer1', '3acfb4b15a93d23e3446d2e97f5cc9e6ba5ef4b83e34c5aa4f55f8c3b5a8e6e6', 'customer', 'John Doe', 'john@email.com', '9876543210');

-- Insert sample products
INSERT INTO products (product_name, category, price, stock_quantity, unit, description) VALUES
('Gulab Jamun', 'Traditional', 250.00, 50, 'kg', 'Soft and syrupy traditional sweet'),
('Rasgulla', 'Traditional', 200.00, 40, 'kg', 'Spongy cottage cheese balls in sugar syrup'),
('Kaju Katli', 'Premium', 800.00, 25, 'kg', 'Premium cashew fudge'),
('Ladoo', 'Traditional', 300.00, 60, 'kg', 'Round sweet balls made with flour and ghee'),
('Barfi', 'Traditional', 350.00, 35, 'kg', 'Sweet confection from condensed milk'),
('Jalebi', 'Traditional', 180.00, 45, 'kg', 'Deep-fried sweet pretzel'),
('Soan Papdi', 'Premium', 400.00, 30, 'kg', 'Flaky and crispy sweet'),
('Chocolate Barfi', 'Fusion', 450.00, 20, 'kg', 'Modern chocolate-flavored barfi'),
('Milk Cake', 'Premium', 500.00, 15, 'kg', 'Dense milk-based sweet'),
('Peda', 'Traditional', 280.00, 55, 'kg', 'Soft milk-based sweet rounds'),
('Mysore Pak', 'Traditional', 420.00, 28, 'kg', 'Ghee-rich sweet from South India'),
('Coconut Ladoo', 'Traditional', 320.00, 38, 'kg', 'Sweet coconut balls'),
('Mixed Sweets Box', 'Gift', 600.00, 5, 'box', 'Assorted traditional sweets in a gift box'),
('Sugar-Free Barfi', 'Healthy', 550.00, 0, 'kg', 'Diabetic-friendly barfi'),
('Dry Fruit Halwa', 'Premium', 750.00, 18, 'kg', 'Rich halwa loaded with dry fruits');

-- Insert sample customers
INSERT INTO customers (customer_name, phone, email, address) VALUES
('Rajesh Kumar', '9876543210', 'rajesh@email.com', '123 Main Street'),
('Priya Sharma', '9876543211', 'priya@email.com', '456 Park Avenue'),
('Amit Singh', '9876543212', 'amit@email.com', '789 Gandhi Road'),
('Neha Patel', '9876543213', 'neha@email.com', '321 Mall Road'),
('Vikram Reddy', '9876543214', 'vikram@email.com', '654 Station Road');