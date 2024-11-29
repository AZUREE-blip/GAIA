import sqlite3


def update_database_and_add_constraint():
    # Connect to the database
    conn = sqlite3.connect('fashion_brand.db')
    cursor = conn.cursor()

    # Add a UNIQUE constraint to the name column in the products table
    try:
        cursor.execute('PRAGMA foreign_keys=off;')  # Disable foreign keys temporarily
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products_temp (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,  -- Add UNIQUE constraint
                price REAL NOT NULL,
                category TEXT,
                description TEXT,
                stock INTEGER,
                image_url TEXT
            )
        ''')
        cursor.execute('INSERT OR IGNORE INTO products_temp SELECT * FROM products')
        cursor.execute('DROP TABLE products')
        cursor.execute('ALTER TABLE products_temp RENAME TO products')
        cursor.execute('PRAGMA foreign_keys=on;')  # Re-enable foreign keys
        print("UNIQUE constraint added successfully.")
    except sqlite3.OperationalError as e:
        print(f"Error adding UNIQUE constraint: {e}")

    # Sample products to insert
    products = [
        ("beanie", 400, "Outerwear", "functional.", 5, "/static/images/outerwear1.jpg"),
        ("Raincoat", 900, "Outerwear", "A waterproof raincoat.", 8, "/static/images/outerwear2.jpg"),
        ("Casual T-Shirt", 300, "Casual Clothing", "A comfortable T-shirt.", 20, "/static/images/casual1.jpg"),
        ("Jeans", 700, "Casual Clothing", "Classic blue jeans.", 15, "/static/images/casual2.jpg")
    ]

    # Insert products using INSERT OR IGNORE
    try:
        cursor.executemany('''
            INSERT OR IGNORE INTO products (name, price, category, description, stock, image_url)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', products)
        print("Sample data inserted successfully (duplicates ignored).")
    except sqlite3.OperationalError as e:
        print(f"Error inserting sample data: {e}")

    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("Database updated successfully.")


# Run the update function
update_database_and_add_constraint()




