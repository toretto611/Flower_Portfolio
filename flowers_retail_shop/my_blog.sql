-- Table 1: users
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,         -- Unique ID for each user
    username VARCHAR(50) NOT NULL,      -- Login name
    email VARCHAR(100) NOT NULL          -- User email, UNIQUE constraint added later
);

-- Add UNIQUE constraint on users.email
ALTER TABLE users
ADD CONSTRAINT unique_users_email UNIQUE(email);

INSERT INTO users (username, email)
VALUES 
('aliceuser', 'alice@example.com'),
('yogiuser', 'yogi@example.com'),
('booboouser', 'booboo@example.com')
RETURNING user_id;

-- Table 2: user_profiles
CREATE TABLE user_profiles (
    profile_id SERIAL PRIMARY KEY,        -- Unique profile ID
    user_id INT NOT NULL,                 -- FK to users
    profile_picture TEXT                  -- Optional: link to profile image
);

-- Add FK constraint to user_profiles.user_id
ALTER TABLE user_profiles
ADD CONSTRAINT fk_user_profiles_user
FOREIGN KEY (user_id) REFERENCES users(user_id);

-- Table 3: business_owners
CREATE TABLE business_owners (
    owner_id SERIAL PRIMARY KEY,           -- Unique ID for each owner
    user_id INT NOT NULL,                   -- FK to users (1-to-1)
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL             -- UNIQUE constraint added later
);

-- Add UNIQUE constraint on business_owners.user_id (enforces 1-to-1 with users)
ALTER TABLE business_owners
ADD CONSTRAINT unique_business_owners_user UNIQUE(user_id);

-- Add UNIQUE constraint on business_owners.email
ALTER TABLE business_owners
ADD CONSTRAINT unique_business_owners_email UNIQUE(email);

-- Add FK constraint to business_owners.user_id
ALTER TABLE business_owners
ADD CONSTRAINT fk_business_owners_user
FOREIGN KEY (user_id) REFERENCES users(user_id);

-- Table 4: customers
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,         -- Unique ID for each customer
    user_id INT NOT NULL,                   -- FK to users (many customers can link to users)
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL
);

-- Add FK constraint to customers.user_id
ALTER TABLE customers
ADD CONSTRAINT fk_customers_user
FOREIGN KEY (user_id) REFERENCES users(user_id);

-- Table 5: products 
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,          -- Unique product ID
    owner_id INT NOT NULL,                  -- FK to business_owners
    name VARCHAR(100) NOT NULL,             -- Name of product (e.g., "Rose Bouquet")
    price DECIMAL(10, 2) NOT NULL           -- Price in dollars
);

-- Add FK constraint to products.owner_id
ALTER TABLE products
ADD CONSTRAINT fk_products_owner
FOREIGN KEY (owner_id) REFERENCES business_owners(owner_id);

-- Table 6: suppliers
CREATE TABLE suppliers (
    supplier_id SERIAL PRIMARY KEY,         -- Unique supplier ID
    owner_id INT NOT NULL,                  -- FK to business_owners
    name VARCHAR(100) NOT NULL,
    contact_name VARCHAR(100),
    email VARCHAR(100) NOT NULL             -- UNIQUE constraint added later
);

-- Add UNIQUE constraint on suppliers.email
ALTER TABLE suppliers
ADD CONSTRAINT unique_suppliers_email UNIQUE(email);

-- Add FK constraint to suppliers.owner_id
ALTER TABLE suppliers
ADD CONSTRAINT fk_suppliers_owner
FOREIGN KEY (owner_id) REFERENCES business_owners(owner_id);

-- Table 7: supplies
CREATE TABLE supplies (
    supply_id SERIAL PRIMARY KEY,           -- Unique supply record ID
    supplier_id INT NOT NULL,               -- FK to suppliers
    product_id INT NOT NULL,                -- FK to products
    cost DECIMAL(10, 2) NOT NULL,           -- Cost charged by supplier
    delivery_date DATE NOT NULL              -- Delivery date of the supply
);

-- Add FK constraints to supplies
ALTER TABLE supplies
ADD CONSTRAINT fk_supplies_supplier
FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id);

ALTER TABLE supplies
ADD CONSTRAINT fk_supplies_product
FOREIGN KEY (product_id) REFERENCES products(product_id);

-- Table 8: orders
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,           -- Unique order ID
    customer_id INT NOT NULL,              -- FK to customers
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add FK constraint to orders.customer_id
ALTER TABLE orders
ADD CONSTRAINT fk_orders_customer
FOREIGN KEY (customer_id) REFERENCES customers(customer_id);

-- Table 9: order_items (each order can have many products)
CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,       -- Unique order item ID
    order_id INT NOT NULL,                  -- FK to orders
    product_id INT NOT NULL,                -- FK to products
    quantity INT NOT NULL DEFAULT 1,
    cost DECIMAL(10, 2) NOT NULL            -- Unit cost at time of purchase
);

-- Add FK constraints to order_items
ALTER TABLE order_items
ADD CONSTRAINT fk_order_items_order
FOREIGN KEY (order_id) REFERENCES orders(order_id);

ALTER TABLE order_items
ADD CONSTRAINT fk_order_items_product
FOREIGN KEY (product_id) REFERENCES products(product_id);

-- Add CHECK constraint to enforce positive quantity
ALTER TABLE order_items
ADD CONSTRAINT chk_order_items_quantity_positive CHECK (quantity > 0);

-- Index --
CREATE INDEX idx_orders_customer_id
ON orders(customer_id);