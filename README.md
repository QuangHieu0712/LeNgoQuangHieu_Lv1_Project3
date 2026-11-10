# Project 03 – E-commerce OLTP Synthetic Data Generation

## 1. Project Overview

This project focuses on generating synthetic data for an E-commerce Online Transaction Processing (OLTP) system using Python and Faker, then loading the generated data into a PostgreSQL database.

The project simulates an e-commerce business environment with relational data across multiple entities, including brands, categories, sellers, customers, products, and promotions.

The generated dataset is designed to maintain referential integrity and follow the business rules defined in the project requirements.

**Project Scope:**
- Generate synthetic data using Python and Faker.
- Design and implement a relational database schema.
- Establish relationships between tables using Primary Keys and Foreign Keys.
- Load generated data into PostgreSQL.
- Validate data consistency and integrity.
- Prepare the dataset for downstream SQL operations in Project 04.

## 2. Objectives

The main objectives of this project are:

- Practice synthetic data generation using Python and Faker.
- Apply relational database concepts in an E-commerce OLTP system.
- Implement database constraints and relationships.
- Handle Python-to-PostgreSQL data integration.
- Generate realistic test data with consistent data types.
- Implement audit columns for data tracking.
- Perform data quality checks to ensure dataset reliability.

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data generation and database interaction |
| Faker | Synthetic data generation |
| PostgreSQL | Relational database management |
| psycopg2 | Python–PostgreSQL connectivity |
| PyCharm | Python development environment |
| SQL | Database creation, insertion, and validation |

## 4. Database Design

The project implements an E-commerce OLTP database consisting of 9 tables.

### 4.1 Core Tables

| Table | Description |
|---|---|
| `brand` | Stores brand information. |
| `category` | Stores product categories and hierarchical relationships. |
| `seller` | Stores seller and shop information. |
| `customer` | Stores customer information. |
| `product` | Stores product details and relationships with brands, categories, and sellers. |
| `promotion` | Stores promotional campaign information. |
| `promotion_product` | Maps promotions to products. |
| `"order"` | Stores customer order information. |
| `order_item` | Stores individual items belonging to each order. |

### 4.2 Relationships

The database follows a relational structure:

- One brand can be associated with multiple products.
- One category can contain multiple products.
- Categories support a two-level hierarchy: parent and child categories.
- One seller can sell multiple products.
- One customer can place multiple orders.
- One order can contain multiple order items.
- One product can appear in multiple order items.
- Promotions and products have a many-to-many relationship through `promotion_product`.

### 4.3 Audit Columns

In addition to the original schema, all tables include the following audit columns:

| Column | Description |
|---|---|
| `created_at` | Timestamp when the record was created. |
| `created_by` | User or system that created the record. |
| `updated_at` | Timestamp of the latest update. |
| `updated_by` | User or system that performed the latest update. |
| `is_deleted` | Indicates whether the record has been soft-deleted. |
| `deleted_at` | Timestamp when the record was deleted. |
| `deleted_by` | User or system that deleted the record. |

These columns support basic data auditing and soft-delete functionality.

## 5. Expected Data Volume

The project generates synthetic data for 7 tables.

| Table | Expected Records | Description |
|---|---:|---|
| `brand` | 20 | Brand information |
| `category` | 25 | 5 parent categories and 20 subcategories |
| `seller` | 50 | Vietnam-based sellers |
| `customer` | 30,000 | Customer information |
| `product` | 3,000 | Product information |
| `promotion` | 30 | Promotional campaigns |
| `promotion_product` | 500 | Promotion-product mappings |
| **Total** | **33,625** | **Synthetic records** |

**Data Time Window:** January 2025 – May 2025.

**Note:** The `order` and `order_item` tables are part of the database schema but their data generation is deferred to Project 04 (SQL), according to the project requirements and instructor's guidance.

## 6. Data Generation Process

The data generation process is implemented using Python and Faker.

### 6.1 Brand Data Generation

- Generate 20 unique brand names.
- Generate country information.
- Insert generated records into the `brand` table.

### 6.2 Category Data Generation

- Generate 5 parent categories.
- Generate 20 child categories.
- Assign each child category to an existing parent category.
- Maintain the category hierarchy using a self-referencing Foreign Key.

### 6.3 Seller Data Generation

- Generate 50 seller records.
- Generate seller names, joining dates, seller types, and ratings.
- Set seller country to Vietnam.

### 6.4 Customer Data Generation

- Generate 30,000 customer records.
- Generate customer names, unique email addresses, phone numbers, gender, addresses, and cities.
- Generate registration timestamps within the project time window.
- Insert records in batches to improve database insertion efficiency.

### 6.5 Product Data Generation

- Generate 3,000 product records.
- Generate product names, prices, stock quantities, ratings, and active statuses.
- Retrieve existing IDs from `brand`, `category`, and `seller`.
- Assign valid Foreign Keys to each product.
- Insert records in batches.

### 6.6 Promotion Data Generation

- Generate 30 promotional campaigns.
- Generate promotion names and promotion types.
- Support two discount types: `percentage` and `fixed_amount`.
- Generate discount values according to the discount type.
- Ensure that `start_date` is not earlier than the date portion of `created_at`.
- Ensure that `end_date` is not earlier than `start_date`.

### 6.7 Promotion-Product Mapping Generation

- Generate 500 promotion-product relationships.
- Retrieve existing promotion and product IDs.
- Ensure each promotion-product pair is unique.
- Maintain referential integrity through Foreign Keys.

## 7. Data Quality and Validation

After data generation, SQL queries are used to validate the dataset.

### 7.1 Record Count Validation

Verify that each table contains the expected number of records.

```sql
SELECT 'brand' AS table_name, COUNT(*) AS total FROM brand
UNION ALL
SELECT 'category', COUNT(*) FROM category
UNION ALL
SELECT 'seller', COUNT(*) FROM seller
UNION ALL
SELECT 'customer', COUNT(*) FROM customer
UNION ALL
SELECT 'product', COUNT(*) FROM product
UNION ALL
SELECT 'promotion', COUNT(*) FROM promotion
UNION ALL
SELECT 'promotion_product', COUNT(*) FROM promotion_product;
```

### 7.2 Foreign Key Validation

Check whether products reference valid brands, categories, and sellers.

```sql
SELECT COUNT(*) AS invalid_product
FROM product p
LEFT JOIN brand b ON p.brand_id = b.brand_id
LEFT JOIN category c ON p.category_id = c.category_id
LEFT JOIN seller s ON p.seller_id = s.seller_id
WHERE b.brand_id IS NULL
   OR c.category_id IS NULL
   OR s.seller_id IS NULL;
```

Check promotion-product relationships:

```sql
SELECT COUNT(*) AS invalid_promotion_product
FROM promotion_product pp
LEFT JOIN promotion p
    ON pp.promotion_id = p.promotion_id
LEFT JOIN product pr
    ON pp.product_id = pr.product_id
WHERE p.promotion_id IS NULL
   OR pr.product_id IS NULL;
```

Expected result: `0` invalid records.

### 7.3 Duplicate Validation

Check duplicate email addresses:

```sql
SELECT email, COUNT(*)
FROM customer
GROUP BY email
HAVING COUNT(*) > 1;
```

Check duplicate phone numbers:

```sql
SELECT phone, COUNT(*)
FROM customer
GROUP BY phone
HAVING COUNT(*) > 1;
```

Check duplicate promotion-product combinations:

```sql
SELECT promotion_id, product_id, COUNT(*)
FROM promotion_product
GROUP BY promotion_id, product_id
HAVING COUNT(*) > 1;
```

Expected result: no duplicate records.

### 7.4 Audit Column Validation

Audit columns are also checked to ensure that required creation metadata is populated.

Example:

```sql
SELECT
    COUNT(*) AS total,
    COUNT(created_at) AS created_at_count,
    COUNT(created_by) AS created_by_count,
    COUNT(is_deleted) AS is_deleted_count
FROM customer;
```

## 8. Project Structure

The project files are organized by responsibility:

~~~text
LeNgoQuangHieu_Lv1_Project3/
│
├── config/
│   ├── __init__.py
│   └── config.py
├── database/
│   ├── __init__.py
│   └── connect.py
├── data_generation/
│   ├── __init__.py
│   ├── generate_brand.py
│   ├── generate_category.py
│   ├── generate_seller.py
│   ├── generate_customer.py
│   ├── generate_product.py
│   ├── generate_promotion.py
│   └── generate_promotion_product.py
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
~~~

**File descriptions:**

| File | Responsibility |
|---|---|
| config/config.py | Stores PostgreSQL connection configuration. |
| database/connect.py | Establishes PostgreSQL connections. |
| data_generation/ | Contains the scripts that create each dataset. |
| main.py | Runs the generation steps in dependency order. |
| requirements.txt | Lists the Python dependencies. |
| .gitignore | Ignores virtual environments, IDE files, caches, and .env files. |

The database schema is created separately; this repository does not currently include a schema.sql file.

## 9. Installation and Setup

### 9.1 Prerequisites

Make sure the following software is installed:

- Python
- PostgreSQL
- PyCharm (or another Python IDE)

### 9.2 Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the virtual environment on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 9.3 Install Dependencies

Install the project dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

The `requirements.txt` file contains the external libraries used directly by this project:

```text
Faker==40.44.0
psycopg2-binary==2.9.13
```

### 9.4 Configure Database Connection

Update config/config.py with your PostgreSQL connection information:

```python
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "ecommerce",
    "user": "postgres",
    "password": "YOUR_PASSWORD"
}
```

Replace `YOUR_PASSWORD` with your local PostgreSQL password. Do not commit a real password.

**Security note:** config/config.py is tracked by Git. Keep the password as a placeholder in commits; never commit a real database password. For a public portfolio, move credentials to environment variables before sharing the repository.

## 10. Running the Project

Make sure the PostgreSQL database and required tables have been created. Activate the virtual environment, then run the pipeline from the project root:

~~~bash
python main.py
~~~

The entry point runs the generators in dependency order: brand, category, seller, customer, product, promotion, and promotion-product mapping.

To run one generator by itself, use Python module mode from the project root. For example:

~~~bash
python -m data_generation.generate_brand
~~~

Product generation requires brand, category, and seller data. Promotion-product mapping requires both promotion and product data.

## 11. Project Results

The project successfully generates synthetic data for 7 E-commerce tables and loads the records into PostgreSQL.

**Final dataset:**

- 20 brands
- 25 categories
- 50 sellers
- 30,000 customers
- 3,000 products
- 30 promotions
- 500 promotion-product mappings

**Total: 33,625 records.**

The dataset maintains the required relational relationships and supports the business constraints defined in the project schema.

## 12. Future Work

The next stage is Project 04 – SQL, which will build on this database.

Planned activities include:

- Generating 5,000,000 order records.
- Generating 17,500,000 order item records.
- Working with large-scale transactional data.
- Practicing SQL queries and data analysis.
- Exploring monthly table partitioning.

---

**Project:** Project 03 – Python in Data  
**Domain:** E-commerce  
**Database:** PostgreSQL  
**Programming Language:** Python  
**Data Generation Library:** Faker