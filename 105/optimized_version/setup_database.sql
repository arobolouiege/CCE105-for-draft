CREATE DATABASE IF NOT EXISTS sari_sari_store;
USE sari_sari_store;

CREATE TABLE IF NOT EXISTS category (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS supplier (
    supplier_id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_name VARCHAR(150) NOT NULL,
    contact_no VARCHAR(50),
    address VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS employee (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS product (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT NOT NULL,
    product_name VARCHAR(150) NOT NULL,
    unit VARCHAR(50) NOT NULL DEFAULT 'piece',
    price DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    reorder_level INT NOT NULL DEFAULT 5,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_product_category
        FOREIGN KEY (category_id) REFERENCES category(category_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS stock_batch (
    stock_batch_id INT AUTO_INCREMENT PRIMARY KEY,
    reference_number VARCHAR(100) NOT NULL,
    supplier_id INT NOT NULL,
    employee_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    cost_per_unit DECIMAL(10,2) NOT NULL,
    stockin_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_stock_supplier
        FOREIGN KEY (supplier_id) REFERENCES supplier(supplier_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT fk_stock_employee
        FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT fk_stock_product
        FOREIGN KEY (product_id) REFERENCES product(product_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    quantity_sold INT NOT NULL,
    selling_price DECIMAL(10,2) NOT NULL,
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_sales_product
        FOREIGN KEY (product_id) REFERENCES product(product_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

INSERT IGNORE INTO category (category_name) VALUES
    ('Canned Goods'),
    ('Beverages'),
    ('Snacks'),
    ('Noodles'),
    ('Household');

INSERT INTO employee (full_name)
SELECT 'Cashier'
WHERE NOT EXISTS (SELECT 1 FROM employee WHERE full_name = 'Cashier');

INSERT INTO supplier (supplier_name, contact_no, address)
SELECT 'Default Supplier', '', ''
WHERE NOT EXISTS (SELECT 1 FROM supplier WHERE supplier_name = 'Default Supplier');

INSERT INTO product (category_id, product_name, unit, price, reorder_level)
SELECT c.category_id, seed.product_name, seed.unit, seed.price, seed.reorder_level
FROM (
    SELECT 'Canned Goods' AS category_name, 'Argentina Corned Beef 150g' AS product_name, 'can' AS unit, 38.00 AS price, 10 AS reorder_level UNION ALL
    SELECT 'Canned Goods', 'Argentina Meat Loaf 150g', 'can', 32.00, 10 UNION ALL
    SELECT 'Canned Goods', 'CDO Karne Norte 150g', 'can', 36.00, 10 UNION ALL
    SELECT 'Canned Goods', 'CDO Meat Loaf 150g', 'can', 30.00, 10 UNION ALL
    SELECT 'Canned Goods', 'Century Tuna Flakes 180g', 'can', 48.00, 8 UNION ALL
    SELECT 'Canned Goods', '555 Sardines Tomato Sauce 155g', 'can', 24.00, 12 UNION ALL
    SELECT 'Canned Goods', 'Ligo Sardines Tomato Sauce 155g', 'can', 25.00, 12 UNION ALL
    SELECT 'Canned Goods', 'Mega Sardines Hot 155g', 'can', 26.00, 12 UNION ALL
    SELECT 'Canned Goods', 'San Marino Corned Tuna 180g', 'can', 45.00, 8 UNION ALL
    SELECT 'Canned Goods', 'Purefoods Corned Beef 150g', 'can', 52.00, 8 UNION ALL
    SELECT 'Canned Goods', 'Holiday Beef Loaf 150g', 'can', 28.00, 10 UNION ALL
    SELECT 'Canned Goods', 'Wow Ulam Afritada 155g', 'can', 31.00, 10 UNION ALL
    SELECT 'Canned Goods', 'Wow Ulam Mechado 155g', 'can', 31.00, 10 UNION ALL
    SELECT 'Canned Goods', 'Youngs Town Sardines 155g', 'can', 23.00, 12 UNION ALL
    SELECT 'Canned Goods', 'Maling Luncheon Meat 397g', 'can', 115.00, 5 UNION ALL
    SELECT 'Canned Goods', 'Spam Lite 340g', 'can', 225.00, 4 UNION ALL
    SELECT 'Canned Goods', 'Libbys Vienna Sausage 130g', 'can', 58.00, 6 UNION ALL
    SELECT 'Canned Goods', 'Del Monte Pineapple Tidbits 234g', 'can', 48.00, 8 UNION ALL
    SELECT 'Beverages', 'Coca-Cola Sakto 200ml', 'bottle', 15.00, 15 UNION ALL
    SELECT 'Beverages', 'Coca-Cola 1.5L', 'bottle', 78.00, 8 UNION ALL
    SELECT 'Beverages', 'Sprite Sakto 200ml', 'bottle', 15.00, 15 UNION ALL
    SELECT 'Beverages', 'Royal Tru-Orange 200ml', 'bottle', 15.00, 15 UNION ALL
    SELECT 'Beverages', 'Pepsi 1.5L', 'bottle', 72.00, 8 UNION ALL
    SELECT 'Beverages', 'Mountain Dew 500ml', 'bottle', 35.00, 10 UNION ALL
    SELECT 'Beverages', 'C2 Green Tea Apple 355ml', 'bottle', 28.00, 10 UNION ALL
    SELECT 'Beverages', 'C2 Green Tea Lemon 355ml', 'bottle', 28.00, 10 UNION ALL
    SELECT 'Beverages', 'Zesto Orange 200ml', 'pack', 12.00, 15 UNION ALL
    SELECT 'Beverages', 'Zesto Mango 200ml', 'pack', 12.00, 15 UNION ALL
    SELECT 'Beverages', 'Chuckie Chocolate Milk 180ml', 'pack', 25.00, 10 UNION ALL
    SELECT 'Beverages', 'Bear Brand Sterilized Milk 200ml', 'can', 36.00, 8 UNION ALL
    SELECT 'Beverages', 'Nescafe Classic Stick 2g', 'sachet', 8.00, 25 UNION ALL
    SELECT 'Beverages', 'Kopiko Brown Coffee Sachet', 'sachet', 9.00, 25 UNION ALL
    SELECT 'Beverages', 'Great Taste White Sachet', 'sachet', 9.00, 25 UNION ALL
    SELECT 'Beverages', 'Milo Sachet 22g', 'sachet', 11.00, 25 UNION ALL
    SELECT 'Beverages', 'Absolute Water 500ml', 'bottle', 18.00, 12 UNION ALL
    SELECT 'Beverages', 'Wilkins Water 1L', 'bottle', 35.00, 10 UNION ALL
    SELECT 'Snacks', 'Piattos Cheese 40g', 'pack', 18.00, 15 UNION ALL
    SELECT 'Snacks', 'Nova Multigrain 40g', 'pack', 18.00, 15 UNION ALL
    SELECT 'Snacks', 'Chippy BBQ 27g', 'pack', 10.00, 20 UNION ALL
    SELECT 'Snacks', 'Clover Chips Cheese 26g', 'pack', 10.00, 20 UNION ALL
    SELECT 'Snacks', 'Boy Bawang Garlic 100g', 'pack', 22.00, 15 UNION ALL
    SELECT 'Snacks', 'Oishi Prawn Crackers 24g', 'pack', 9.00, 20 UNION ALL
    SELECT 'Snacks', 'Martys Cracklin Salt Vinegar 26g', 'pack', 12.00, 20 UNION ALL
    SELECT 'Snacks', 'Mang Juan Chicharron 26g', 'pack', 12.00, 20 UNION ALL
    SELECT 'Snacks', 'SkyFlakes Crackers 25g', 'pack', 8.00, 25 UNION ALL
    SELECT 'Snacks', 'Fita Crackers 30g', 'pack', 9.00, 25 UNION ALL
    SELECT 'Snacks', 'Rebisco Crackers 32g', 'pack', 8.00, 25 UNION ALL
    SELECT 'Snacks', 'Hansel Chocolate 30g', 'pack', 9.00, 25 UNION ALL
    SELECT 'Snacks', 'Presto Creams Peanut Butter 30g', 'pack', 9.00, 25 UNION ALL
    SELECT 'Snacks', 'Cloud 9 Classic 28g', 'piece', 10.00, 20 UNION ALL
    SELECT 'Snacks', 'Nips Chocolate 40g', 'pack', 18.00, 15 UNION ALL
    SELECT 'Snacks', 'Moby Caramel 40g', 'pack', 12.00, 20 UNION ALL
    SELECT 'Snacks', 'Ding Dong Mixed Nuts 100g', 'pack', 24.00, 15 UNION ALL
    SELECT 'Snacks', 'Tom Sawyer Popcorn 100g', 'pack', 20.00, 15 UNION ALL
    SELECT 'Noodles', 'Lucky Me Pancit Canton Original', 'pack', 16.00, 20 UNION ALL
    SELECT 'Noodles', 'Lucky Me Pancit Canton Chilimansi', 'pack', 16.00, 20 UNION ALL
    SELECT 'Noodles', 'Lucky Me Pancit Canton Sweet Spicy', 'pack', 16.00, 20 UNION ALL
    SELECT 'Noodles', 'Lucky Me Beef Noodles', 'pack', 14.00, 20 UNION ALL
    SELECT 'Noodles', 'Lucky Me Chicken Noodles', 'pack', 14.00, 20 UNION ALL
    SELECT 'Noodles', 'Lucky Me Bulalo Noodles', 'pack', 14.00, 20 UNION ALL
    SELECT 'Noodles', 'Payless Pancit Canton Xtra Big', 'pack', 18.00, 18 UNION ALL
    SELECT 'Noodles', 'Payless Beef Noodles', 'pack', 13.00, 20 UNION ALL
    SELECT 'Noodles', 'Nissin Ramen Beef', 'pack', 15.00, 20 UNION ALL
    SELECT 'Noodles', 'Nissin Ramen Seafood', 'pack', 15.00, 20 UNION ALL
    SELECT 'Noodles', 'Quickchow Pancit Canton', 'pack', 14.00, 20 UNION ALL
    SELECT 'Noodles', 'Ho-Mi Instant Mami Beef', 'pack', 12.00, 20 UNION ALL
    SELECT 'Noodles', 'Maggi Magic Sarap Noodles', 'pack', 13.00, 20 UNION ALL
    SELECT 'Noodles', 'Nissin Cup Noodles Beef', 'cup', 38.00, 10 UNION ALL
    SELECT 'Noodles', 'Nissin Cup Noodles Seafood', 'cup', 38.00, 10 UNION ALL
    SELECT 'Noodles', 'Lucky Me Supreme Bulalo Cup', 'cup', 42.00, 10 UNION ALL
    SELECT 'Noodles', 'Lucky Me Supreme La Paz Batchoy Cup', 'cup', 42.00, 10 UNION ALL
    SELECT 'Noodles', 'Jin Ramen Mild 120g', 'pack', 52.00, 8 UNION ALL
    SELECT 'Household', 'Surf Powder Kalamansi 70g', 'sachet', 9.00, 25 UNION ALL
    SELECT 'Household', 'Ariel Powder 70g', 'sachet', 10.00, 25 UNION ALL
    SELECT 'Household', 'Tide Powder 70g', 'sachet', 10.00, 25 UNION ALL
    SELECT 'Household', 'Champion Detergent Bar 380g', 'bar', 28.00, 12 UNION ALL
    SELECT 'Household', 'Perla White Laundry Soap 110g', 'bar', 22.00, 12 UNION ALL
    SELECT 'Household', 'Safeguard White 60g', 'bar', 32.00, 10 UNION ALL
    SELECT 'Household', 'Bioderm Germicidal Soap 60g', 'bar', 25.00, 10 UNION ALL
    SELECT 'Household', 'Palmolive Shampoo Sachet', 'sachet', 8.00, 25 UNION ALL
    SELECT 'Household', 'Cream Silk Conditioner Sachet', 'sachet', 8.00, 25 UNION ALL
    SELECT 'Household', 'Head and Shoulders Sachet', 'sachet', 9.00, 25 UNION ALL
    SELECT 'Household', 'Colgate Toothpaste Sachet', 'sachet', 8.00, 25 UNION ALL
    SELECT 'Household', 'Closeup Toothpaste Sachet', 'sachet', 8.00, 25 UNION ALL
    SELECT 'Household', 'Joy Dishwashing Liquid Sachet', 'sachet', 7.00, 25 UNION ALL
    SELECT 'Household', 'Zonrox Bleach 250ml', 'bottle', 28.00, 10 UNION ALL
    SELECT 'Household', 'Baygon Mosquito Coil 10s', 'pack', 32.00, 8 UNION ALL
    SELECT 'Household', 'Tissue Roll 2-Ply', 'roll', 12.00, 20 UNION ALL
    SELECT 'Household', 'Garbage Bag Small 10s', 'pack', 25.00, 10 UNION ALL
    SELECT 'Household', 'Matchbox Pack', 'pack', 6.00, 20 UNION ALL
    SELECT 'Canned Goods', 'Reno Liver Spread 85g', 'can', 27.00, 10 UNION ALL
    SELECT 'Beverages', 'Tang Orange Sachet 25g', 'sachet', 12.00, 20 UNION ALL
    SELECT 'Snacks', 'Jack n Jill Pretzels 28g', 'pack', 11.00, 20
) seed
JOIN category c ON c.category_name = seed.category_name
WHERE NOT EXISTS (
    SELECT 1 FROM product p WHERE p.product_name = seed.product_name
);

INSERT INTO product (category_id, product_name, unit, price, reorder_level)
SELECT
    c.category_id,
    CONCAT('Store Product ', LPAD(nums.n, 3, '0')),
    CASE MOD(nums.n, 5)
        WHEN 0 THEN 'can'
        WHEN 1 THEN 'bottle'
        WHEN 2 THEN 'pack'
        WHEN 3 THEN 'pack'
        ELSE 'piece'
    END AS unit,
    10.00 + MOD(nums.n * 7, 95) AS price,
    5 + MOD(nums.n, 21) AS reorder_level
FROM (
    SELECT hundreds.d * 100 + tens.d * 10 + ones.d + 1 AS n
    FROM (
        SELECT 0 AS d UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
        UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9
    ) hundreds
    CROSS JOIN (
        SELECT 0 AS d UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
        UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9
    ) tens
    CROSS JOIN (
        SELECT 0 AS d UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
        UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9
    ) ones
) nums
JOIN category c ON c.category_name = CASE MOD(nums.n, 5)
    WHEN 0 THEN 'Canned Goods'
    WHEN 1 THEN 'Beverages'
    WHEN 2 THEN 'Snacks'
    WHEN 3 THEN 'Noodles'
    ELSE 'Household'
END
WHERE nums.n BETWEEN 1 AND 200
  AND NOT EXISTS (
      SELECT 1
      FROM product p
      WHERE p.product_name = CONCAT('Store Product ', LPAD(nums.n, 3, '0'))
  );

INSERT INTO product (category_id, product_name, unit, price, reorder_level)
SELECT c.category_id, seed.product_name, seed.unit, seed.price, seed.reorder_level
FROM (
    SELECT 'Canned Goods' AS category_name, 'Century Tuna Hot and Spicy 180g' AS product_name, 'can' AS unit, 49.00 AS price, 8 AS reorder_level UNION ALL
    SELECT 'Canned Goods', 'Century Tuna Calamansi 180g', 'can', 49.00, 8 UNION ALL
    SELECT 'Canned Goods', '555 Tuna Afritada 155g', 'can', 34.00, 10 UNION ALL
    SELECT 'Canned Goods', '555 Tuna Caldereta 155g', 'can', 34.00, 10 UNION ALL
    SELECT 'Canned Goods', '555 Tuna Mechado 155g', 'can', 34.00, 10 UNION ALL
    SELECT 'Canned Goods', 'Mega Sardines Spanish Style 155g', 'can', 29.00, 12 UNION ALL
    SELECT 'Canned Goods', 'Mega Sardines Tomato Sauce 425g', 'can', 62.00, 8 UNION ALL
    SELECT 'Canned Goods', 'Ligo Sardines Gata 155g', 'can', 29.00, 12 UNION ALL
    SELECT 'Canned Goods', 'Ligo Sardines Chili 155g', 'can', 26.00, 12 UNION ALL
    SELECT 'Canned Goods', 'Saba Mackerel 155g', 'can', 35.00, 10 UNION ALL
    SELECT 'Canned Goods', 'Saba Mackerel 425g', 'can', 78.00, 6 UNION ALL
    SELECT 'Canned Goods', 'Rose Bowl Sardines 155g', 'can', 28.00, 12 UNION ALL
    SELECT 'Canned Goods', 'Master Sardines 155g', 'can', 24.00, 12 UNION ALL
    SELECT 'Canned Goods', 'Blue Bay Tuna Flakes 155g', 'can', 38.00, 10 UNION ALL
    SELECT 'Canned Goods', 'Fresca Tuna Flakes 175g', 'can', 42.00, 8 UNION ALL
    SELECT 'Canned Goods', 'San Marino Chili Corned Tuna 180g', 'can', 46.00, 8 UNION ALL
    SELECT 'Canned Goods', 'Century Bangus Belly Spanish Style 184g', 'can', 92.00, 5 UNION ALL
    SELECT 'Canned Goods', 'Uni-Pak Mackerel 155g', 'can', 32.00, 10 UNION ALL
    SELECT 'Canned Goods', 'Gold Seas Tuna Chunks 185g', 'can', 58.00, 8 UNION ALL
    SELECT 'Canned Goods', 'Del Monte Fruit Cocktail 432g', 'can', 88.00, 6 UNION ALL
    SELECT 'Canned Goods', 'RAM Pork and Beans 230g', 'can', 36.00, 10 UNION ALL
    SELECT 'Canned Goods', 'Hunts Pork and Beans 230g', 'can', 39.00, 10 UNION ALL
    SELECT 'Canned Goods', 'Swift Vienna Sausage 130g', 'can', 44.00, 8 UNION ALL
    SELECT 'Canned Goods', 'Purefoods Vienna Sausage 130g', 'can', 50.00, 8 UNION ALL
    SELECT 'Canned Goods', 'Highlands Gold Corned Beef 150g', 'can', 55.00, 8 UNION ALL
    SELECT 'Canned Goods', 'Star Corned Beef 150g', 'can', 35.00, 10 UNION ALL
    SELECT 'Canned Goods', 'Palm Corned Beef 326g', 'can', 145.00, 5 UNION ALL
    SELECT 'Canned Goods', 'Ox and Palm Corned Beef 326g', 'can', 155.00, 5 UNION ALL
    SELECT 'Canned Goods', 'Ma Ling Pork Luncheon Meat 397g', 'can', 128.00, 5 UNION ALL
    SELECT 'Canned Goods', 'Tulip Luncheon Meat 340g', 'can', 138.00, 5 UNION ALL
    SELECT 'Canned Goods', 'Prem Luncheon Meat 340g', 'can', 125.00, 5 UNION ALL
    SELECT 'Canned Goods', 'CDO Ulam Burger Steak 155g', 'can', 34.00, 10 UNION ALL
    SELECT 'Canned Goods', 'CDO Ulam Sisig 155g', 'can', 34.00, 10 UNION ALL
    SELECT 'Canned Goods', 'Argentina Beef Loaf 150g', 'can', 31.00, 10 UNION ALL
    SELECT 'Canned Goods', 'Argentina Chicken Loaf 150g', 'can', 30.00, 10 UNION ALL
    SELECT 'Canned Goods', 'Purefoods Liver Spread 85g', 'can', 32.00, 10 UNION ALL
    SELECT 'Canned Goods', 'Lady Choice Tuna Spread 80g', 'jar', 45.00, 8 UNION ALL
    SELECT 'Canned Goods', 'Angel Kremdensada 410ml', 'can', 54.00, 8 UNION ALL
    SELECT 'Canned Goods', 'Alaska Condensada 300ml', 'can', 49.00, 8 UNION ALL
    SELECT 'Canned Goods', 'Carnation Evaporada 370ml', 'can', 55.00, 8 UNION ALL
    SELECT 'Beverages', 'Milo Ready-to-Drink 180ml', 'pack', 27.00, 12 UNION ALL
    SELECT 'Beverages', 'Nescafe Creamy White Sachet 27g', 'sachet', 10.00, 25 UNION ALL
    SELECT 'Beverages', 'San Mig Coffee Original Sachet', 'sachet', 9.00, 25 UNION ALL
    SELECT 'Beverages', 'Blend 45 Coffee Sachet', 'sachet', 8.00, 25 UNION ALL
    SELECT 'Beverages', 'Energen Chocolate Sachet', 'sachet', 10.00, 25 UNION ALL
    SELECT 'Beverages', 'Swiss Miss Milk Chocolate Sachet', 'sachet', 18.00, 20 UNION ALL
    SELECT 'Beverages', 'Tang Mango Sachet 25g', 'sachet', 12.00, 20 UNION ALL
    SELECT 'Beverages', 'Nestea Iced Tea Lemon Sachet', 'sachet', 18.00, 20 UNION ALL
    SELECT 'Beverages', 'Eight O Clock Orange Juice 250ml', 'pack', 16.00, 15 UNION ALL
    SELECT 'Beverages', 'Minute Maid Pulpy Orange 330ml', 'bottle', 32.00, 10 UNION ALL
    SELECT 'Beverages', 'Tropicana Twister Orange 355ml', 'bottle', 35.00, 10 UNION ALL
    SELECT 'Beverages', 'Del Monte Pineapple Juice 240ml', 'can', 30.00, 10 UNION ALL
    SELECT 'Beverages', 'Dole Pineapple Juice 240ml', 'can', 30.00, 10 UNION ALL
    SELECT 'Beverages', 'Vitamilk Soy Drink 300ml', 'bottle', 38.00, 10 UNION ALL
    SELECT 'Beverages', 'Dutch Mill Yogurt Drink 180ml', 'pack', 24.00, 12 UNION ALL
    SELECT 'Beverages', 'Yakult Cultured Milk 80ml', 'bottle', 13.00, 20 UNION ALL
    SELECT 'Beverages', 'Gatorade Blue Bolt 500ml', 'bottle', 45.00, 10 UNION ALL
    SELECT 'Beverages', 'Pocari Sweat 500ml', 'bottle', 52.00, 8 UNION ALL
    SELECT 'Beverages', 'Sting Energy Drink 330ml', 'bottle', 25.00, 12 UNION ALL
    SELECT 'Beverages', 'Cobra Energy Drink 350ml', 'bottle', 25.00, 12 UNION ALL
    SELECT 'Beverages', 'Red Bull Energy Drink 250ml', 'can', 75.00, 6 UNION ALL
    SELECT 'Beverages', 'Summit Water 500ml', 'bottle', 16.00, 12 UNION ALL
    SELECT 'Beverages', 'Nature Spring Water 500ml', 'bottle', 16.00, 12 UNION ALL
    SELECT 'Beverages', 'Viva Mineral Water 500ml', 'bottle', 15.00, 12 UNION ALL
    SELECT 'Beverages', 'Absolute Distilled Water 1L', 'bottle', 32.00, 10 UNION ALL
    SELECT 'Beverages', 'Wilkins Pure Water 500ml', 'bottle', 19.00, 12 UNION ALL
    SELECT 'Beverages', 'Sola Iced Tea Lemon 473ml', 'bottle', 42.00, 8 UNION ALL
    SELECT 'Beverages', 'Lipton Iced Tea Lemon 500ml', 'bottle', 40.00, 8 UNION ALL
    SELECT 'Beverages', 'Nestea Lemon Ready-to-Drink 500ml', 'bottle', 38.00, 8 UNION ALL
    SELECT 'Beverages', 'Ovaltine Chocolate Malt Sachet', 'sachet', 12.00, 25 UNION ALL
    SELECT 'Beverages', 'Bear Brand Powdered Milk Sachet 33g', 'sachet', 14.00, 25 UNION ALL
    SELECT 'Beverages', 'Alaska Powdered Milk Sachet 33g', 'sachet', 13.00, 25 UNION ALL
    SELECT 'Beverages', 'Birch Tree Fortified Milk Sachet 33g', 'sachet', 13.00, 25 UNION ALL
    SELECT 'Beverages', 'Chuckie Chocolate Milk 250ml', 'pack', 32.00, 10 UNION ALL
    SELECT 'Beverages', 'Selecta Fortified Milk 250ml', 'pack', 30.00, 10 UNION ALL
    SELECT 'Beverages', 'Magnolia Chocolait 250ml', 'pack', 32.00, 10 UNION ALL
    SELECT 'Beverages', 'Dutch Mill Delight 400ml', 'bottle', 40.00, 8 UNION ALL
    SELECT 'Beverages', 'Mogu Mogu Lychee 320ml', 'bottle', 42.00, 8 UNION ALL
    SELECT 'Beverages', 'Zesto Dalandan 200ml', 'pack', 12.00, 15 UNION ALL
    SELECT 'Beverages', 'RC Cola 1.5L', 'bottle', 68.00, 8 UNION ALL
    SELECT 'Snacks', 'Lays Classic Salted 50g', 'pack', 45.00, 8 UNION ALL
    SELECT 'Snacks', 'Doritos Nacho Cheese 65g', 'pack', 52.00, 8 UNION ALL
    SELECT 'Snacks', 'Cheetos Crunchy Cheese 60g', 'pack', 50.00, 8 UNION ALL
    SELECT 'Snacks', 'Roller Coaster Potato Rings 60g', 'pack', 20.00, 15 UNION ALL
    SELECT 'Snacks', 'Mr Chips Nacho Cheese 100g', 'pack', 28.00, 12 UNION ALL
    SELECT 'Snacks', 'Tostillas Barbecue 100g', 'pack', 28.00, 12 UNION ALL
    SELECT 'Snacks', 'Vcut Spicy Barbecue 60g', 'pack', 24.00, 12 UNION ALL
    SELECT 'Snacks', 'Potato Fries Cheese 50g', 'pack', 18.00, 15 UNION ALL
    SELECT 'Snacks', 'Snacku Vegetable Crackers 60g', 'pack', 18.00, 15 UNION ALL
    SELECT 'Snacks', 'Bread Pan Toasted Bread 42g', 'pack', 15.00, 15 UNION ALL
    SELECT 'Snacks', 'Nagaraya Garlic Cracker Nuts 80g', 'pack', 25.00, 15 UNION ALL
    SELECT 'Snacks', 'Growers Peanuts Garlic 80g', 'pack', 28.00, 12 UNION ALL
    SELECT 'Snacks', 'Sugo Peanuts Garlic 80g', 'pack', 22.00, 15 UNION ALL
    SELECT 'Snacks', 'Happy Peanuts Garlic 80g', 'pack', 20.00, 15 UNION ALL
    SELECT 'Snacks', 'Butter Coconut Biscuit 150g', 'pack', 35.00, 10 UNION ALL
    SELECT 'Snacks', 'Magic Flakes Plain 30g', 'pack', 8.00, 25 UNION ALL
    SELECT 'Snacks', 'Dewberry Strawberry 33g', 'pack', 9.00, 25 UNION ALL
    SELECT 'Snacks', 'Cream-O Chocolate 33g', 'pack', 10.00, 25 UNION ALL
    SELECT 'Snacks', 'Oreo Vanilla 29g', 'pack', 12.00, 20 UNION ALL
    SELECT 'Snacks', 'Tiger Energy Biscuit 30g', 'pack', 8.00, 25 UNION ALL
    SELECT 'Snacks', 'Quake Overload Chocolate 30g', 'pack', 10.00, 20 UNION ALL
    SELECT 'Snacks', 'Loacker Quadratini Napolitaner 125g', 'pack', 95.00, 5 UNION ALL
    SELECT 'Snacks', 'Stick-O Chocolate Wafer Stick 380g', 'can', 105.00, 5 UNION ALL
    SELECT 'Snacks', 'Hello Chocolate Wafer 38g', 'pack', 12.00, 20 UNION ALL
    SELECT 'Snacks', 'Knick Knacks Chocolate 28g', 'pack', 9.00, 25 UNION ALL
    SELECT 'Snacks', 'Pillows Ube Filled Crackers 38g', 'pack', 12.00, 20 UNION ALL
    SELECT 'Snacks', 'Flat Tops Chocolate 100g', 'pack', 45.00, 10 UNION ALL
    SELECT 'Snacks', 'Curly Tops Chocolate 100g', 'pack', 48.00, 10 UNION ALL
    SELECT 'Snacks', 'Choc Nut Peanut Milk Chocolate 24s', 'pack', 60.00, 8 UNION ALL
    SELECT 'Snacks', 'Judge Bubble Gum 50s', 'jar', 55.00, 8 UNION ALL
    SELECT 'Snacks', 'Maxx Honey Lemon Candy 50s', 'pack', 50.00, 8 UNION ALL
    SELECT 'Snacks', 'Snowbear Menthol Candy 50s', 'pack', 50.00, 8 UNION ALL
    SELECT 'Snacks', 'Mentos Mint Roll 37g', 'roll', 28.00, 12 UNION ALL
    SELECT 'Snacks', 'Hany Milk Chocolate 24s', 'pack', 62.00, 8 UNION ALL
    SELECT 'Snacks', 'Lala Chocolate 24s', 'pack', 58.00, 8 UNION ALL
    SELECT 'Snacks', 'Choco Mucho Classic 32g', 'piece', 14.00, 20 UNION ALL
    SELECT 'Snacks', 'Bingo Chocolate Cookie Sandwich 28g', 'pack', 9.00, 25 UNION ALL
    SELECT 'Snacks', 'Loaded White Chocolate 32g', 'pack', 10.00, 20 UNION ALL
    SELECT 'Snacks', 'Superstix Chocolate Wafer Stick 40g', 'pack', 12.00, 20 UNION ALL
    SELECT 'Snacks', 'Cloud 9 Overload 42g', 'piece', 18.00, 15 UNION ALL
    SELECT 'Noodles', 'Lucky Me Pancit Canton Kalamansi', 'pack', 16.00, 20 UNION ALL
    SELECT 'Noodles', 'Lucky Me Pancit Canton Hot Chili', 'pack', 16.00, 20 UNION ALL
    SELECT 'Noodles', 'Lucky Me Pancit Canton Extra Hot Chili', 'pack', 16.00, 20 UNION ALL
    SELECT 'Noodles', 'Lucky Me Pancit Canton Chilimansi Big', 'pack', 28.00, 15 UNION ALL
    SELECT 'Noodles', 'Payless Xtra Big Kalamansi', 'pack', 18.00, 18 UNION ALL
    SELECT 'Noodles', 'Quickchow Pancit Canton Kalamansi', 'pack', 14.00, 20 UNION ALL
    SELECT 'Noodles', 'Yakisoba Savory Beef', 'pack', 18.00, 18 UNION ALL
    SELECT 'Noodles', 'Yakisoba Spicy Chicken', 'pack', 18.00, 18 UNION ALL
    SELECT 'Noodles', 'Nissin Yakisoba Spicy Chicken', 'pack', 20.00, 18 UNION ALL
    SELECT 'Noodles', 'Nissin Yakisoba Savory Beef', 'pack', 20.00, 18 UNION ALL
    SELECT 'Noodles', 'Nissin Ramen Chicken', 'pack', 15.00, 20 UNION ALL
    SELECT 'Noodles', 'Nissin Ramen Spicy Seafood', 'pack', 15.00, 20 UNION ALL
    SELECT 'Noodles', 'Nissin Ramen Hot Beef', 'pack', 15.00, 20 UNION ALL
    SELECT 'Noodles', 'Nissin Cup Seafood Curry', 'cup', 40.00, 10 UNION ALL
    SELECT 'Noodles', 'Lucky Me Cup Noodles Jjamppong', 'cup', 42.00, 10 UNION ALL
    SELECT 'Noodles', 'Lucky Me Cup Noodles Batchoy', 'cup', 40.00, 10 UNION ALL
    SELECT 'Noodles', 'Maggi Rich Mami Chicken', 'pack', 14.00, 20 UNION ALL
    SELECT 'Noodles', 'Maggi Rich Mami Beef', 'pack', 14.00, 20 UNION ALL
    SELECT 'Noodles', 'Ho-Mi Instant Mami Chicken', 'pack', 12.00, 20 UNION ALL
    SELECT 'Noodles', 'Payless Chicken Noodles', 'pack', 13.00, 20 UNION ALL
    SELECT 'Noodles', 'Payless Bulalo Noodles', 'pack', 13.00, 20 UNION ALL
    SELECT 'Noodles', 'Quickchow Beef Mami', 'pack', 13.00, 20 UNION ALL
    SELECT 'Noodles', 'Quickchow Chicken Mami', 'pack', 13.00, 20 UNION ALL
    SELECT 'Noodles', 'Lucky Me Sotanghon Chicken', 'pack', 18.00, 18 UNION ALL
    SELECT 'Noodles', 'Lucky Me Sotanghon Beef', 'pack', 18.00, 18 UNION ALL
    SELECT 'Noodles', 'Lucky Me Lomi Instant Noodles', 'pack', 17.00, 18 UNION ALL
    SELECT 'Noodles', 'Lucky Me Macaroni Soup Chicken', 'pack', 17.00, 18 UNION ALL
    SELECT 'Noodles', 'Nissin Pasta Express Carbonara', 'pack', 32.00, 12 UNION ALL
    SELECT 'Noodles', 'Nissin Pasta Express Spaghetti', 'pack', 32.00, 12 UNION ALL
    SELECT 'Noodles', 'Samyang Buldak Hot Chicken Ramen', 'pack', 72.00, 6 UNION ALL
    SELECT 'Noodles', 'Samyang Carbonara Buldak Ramen', 'pack', 78.00, 6 UNION ALL
    SELECT 'Noodles', 'Nongshim Shin Ramyun 120g', 'pack', 65.00, 8 UNION ALL
    SELECT 'Noodles', 'Nongshim Neoguri 120g', 'pack', 68.00, 8 UNION ALL
    SELECT 'Noodles', 'Ottogi Jin Ramen Spicy 120g', 'pack', 55.00, 8 UNION ALL
    SELECT 'Noodles', 'Indomie Mi Goreng Original', 'pack', 18.00, 18 UNION ALL
    SELECT 'Noodles', 'Indomie Mi Goreng Hot Spicy', 'pack', 18.00, 18 UNION ALL
    SELECT 'Noodles', 'Mi Sedaap Goreng Original', 'pack', 18.00, 18 UNION ALL
    SELECT 'Noodles', 'Wai Wai Chicken Flavor Noodles', 'pack', 16.00, 18 UNION ALL
    SELECT 'Noodles', 'Mama Tom Yum Noodles', 'pack', 25.00, 15 UNION ALL
    SELECT 'Noodles', 'Maruchan Ramen Chicken', 'pack', 42.00, 10 UNION ALL
    SELECT 'Household', 'Downy Sunrise Fresh Sachet', 'sachet', 9.00, 25 UNION ALL
    SELECT 'Household', 'Downy Garden Bloom Sachet', 'sachet', 9.00, 25 UNION ALL
    SELECT 'Household', 'Surf Liquid Detergent Sachet', 'sachet', 10.00, 25 UNION ALL
    SELECT 'Household', 'Ariel Liquid Detergent Sachet', 'sachet', 11.00, 25 UNION ALL
    SELECT 'Household', 'Tide Detergent Bar 380g', 'bar', 30.00, 12 UNION ALL
    SELECT 'Household', 'Pride Detergent Bar 380g', 'bar', 26.00, 12 UNION ALL
    SELECT 'Household', 'Breeze Detergent Powder 70g', 'sachet', 10.00, 25 UNION ALL
    SELECT 'Household', 'Calla Detergent Powder 70g', 'sachet', 9.00, 25 UNION ALL
    SELECT 'Household', 'Bonux Detergent Powder 70g', 'sachet', 9.00, 25 UNION ALL
    SELECT 'Household', 'Zonrox Colorsafe Bleach 250ml', 'bottle', 36.00, 10 UNION ALL
    SELECT 'Household', 'Domex Multi-Purpose Cleaner 250ml', 'bottle', 55.00, 8 UNION ALL
    SELECT 'Household', 'Mr Muscle Kitchen Cleaner 250ml', 'bottle', 75.00, 6 UNION ALL
    SELECT 'Household', 'Lysol Disinfectant Spray 340g', 'can', 235.00, 4 UNION ALL
    SELECT 'Household', 'Green Cross Alcohol 250ml', 'bottle', 48.00, 10 UNION ALL
    SELECT 'Household', 'Casino Ethyl Alcohol 250ml', 'bottle', 45.00, 10 UNION ALL
    SELECT 'Household', 'Hygienix Germ Kill Alcohol 250ml', 'bottle', 45.00, 10 UNION ALL
    SELECT 'Household', 'Safeguard Lemon Soap 60g', 'bar', 32.00, 10 UNION ALL
    SELECT 'Household', 'Dove White Beauty Bar 90g', 'bar', 65.00, 8 UNION ALL
    SELECT 'Household', 'Irish Spring Original Soap 90g', 'bar', 55.00, 8 UNION ALL
    SELECT 'Household', 'Palmolive Naturals Soap 90g', 'bar', 42.00, 10 UNION ALL
    SELECT 'Household', 'Johnsons Baby Powder 50g', 'bottle', 42.00, 10 UNION ALL
    SELECT 'Household', 'Silka Papaya Soap 90g', 'bar', 38.00, 10 UNION ALL
    SELECT 'Household', 'Kojie San Skin Lightening Soap 65g', 'bar', 50.00, 8 UNION ALL
    SELECT 'Household', 'Sunsilk Smooth Shampoo Sachet', 'sachet', 8.00, 25 UNION ALL
    SELECT 'Household', 'Dove Shampoo Sachet', 'sachet', 9.00, 25 UNION ALL
    SELECT 'Household', 'Clear Men Shampoo Sachet', 'sachet', 9.00, 25 UNION ALL
    SELECT 'Household', 'Pantene Hair Fall Shampoo Sachet', 'sachet', 9.00, 25 UNION ALL
    SELECT 'Household', 'Rejoice Rich Shampoo Sachet', 'sachet', 8.00, 25 UNION ALL
    SELECT 'Household', 'Colgate Toothpaste 75ml', 'tube', 58.00, 8 UNION ALL
    SELECT 'Household', 'Closeup Toothpaste 75ml', 'tube', 55.00, 8 UNION ALL
    SELECT 'Household', 'Hapee Toothpaste 75ml', 'tube', 42.00, 10 UNION ALL
    SELECT 'Household', 'Sensodyne Fresh Mint 50g', 'tube', 115.00, 5 UNION ALL
    SELECT 'Household', 'Joy Lemon Dishwashing Liquid 250ml', 'bottle', 52.00, 8 UNION ALL
    SELECT 'Household', 'Axion Dishwashing Paste 200g', 'tub', 42.00, 10 UNION ALL
    SELECT 'Household', 'Scotch-Brite Sponge Single', 'piece', 28.00, 10 UNION ALL
    SELECT 'Household', 'Champion Fabric Conditioner Sachet', 'sachet', 8.00, 25 UNION ALL
    SELECT 'Household', 'Surf Fabric Conditioner Sachet', 'sachet', 8.00, 25 UNION ALL
    SELECT 'Household', 'Baygon Aerosol Multi-Insect 250ml', 'can', 165.00, 5 UNION ALL
    SELECT 'Household', 'OFF Lotion Sachet 6ml', 'sachet', 12.00, 20 UNION ALL
    SELECT 'Household', 'Glade Morning Fresh Aerosol 320ml', 'can', 145.00, 5
) seed
JOIN category c ON c.category_name = seed.category_name
WHERE NOT EXISTS (
    SELECT 1 FROM product p WHERE p.product_name = seed.product_name
);

DROP VIEW IF EXISTS vw_low_stock;
CREATE VIEW vw_low_stock AS
SELECT
    p.product_id,
    p.product_name,
    c.category_name,
    p.reorder_level,
    COALESCE(SUM(sb.quantity), 0)
      - COALESCE((
            SELECT SUM(s.quantity_sold)
            FROM sales s
            WHERE s.product_id = p.product_id
        ), 0) AS stock_qty
FROM product p
JOIN category c ON p.category_id = c.category_id
LEFT JOIN stock_batch sb ON sb.product_id = p.product_id
GROUP BY p.product_id, p.product_name, c.category_name, p.reorder_level
HAVING stock_qty <= p.reorder_level;

DROP VIEW IF EXISTS vw_daily_stockin;
CREATE VIEW vw_daily_stockin AS
SELECT
    sb.stockin_date,
    p.product_name,
    sup.supplier_name,
    e.full_name AS received_by,
    sb.quantity,
    sb.cost_per_unit,
    sb.quantity * sb.cost_per_unit AS total_cost
FROM stock_batch sb
JOIN product p ON sb.product_id = p.product_id
JOIN supplier sup ON sb.supplier_id = sup.supplier_id
JOIN employee e ON sb.employee_id = e.employee_id;
