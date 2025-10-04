import mysql.connector
import os
from dotenv import load_dotenv
from utils.security import hash_password

load_dotenv()

# Configuration from .env file
db_config = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE')
}

class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(**db_config)
            self.cursor = self.conn.cursor(dictionary=True)
            print("✅ MySQL Database connected successfully!")
        except mysql.connector.Error as err:
            print(f"❌ Error connecting to MySQL: {err}")
            exit(1)

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

db = Database()
db.connect()

def create_tables_and_seed():
    cursor = db.conn.cursor()
    
    # --- 1. Users Table ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            user_id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            role ENUM('student', 'faculty', 'admin') NOT NULL DEFAULT 'student', 
            phone_number VARCHAR(15),
            password_hash VARCHAR(255) NOT NULL
        )
    """)
    
    # --- 2. Categories Table ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Categories (
            category_id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(50) UNIQUE NOT NULL
        )
    """)
    
    # --- 3. Items Table ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Items (
            item_id INT PRIMARY KEY AUTO_INCREMENT,
            reported_by INT NOT NULL,
            category_id INT NOT NULL,
            title VARCHAR(100) NOT NULL,
            description TEXT,
            status ENUM('lost', 'found', 'claim_pending', 'resolved') NOT NULL,
            image_url VARCHAR(255),
            date_reported DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (reported_by) REFERENCES Users(user_id),
            FOREIGN KEY (category_id) REFERENCES Categories(category_id)
        )
    """)
    
    # --- 4. Claims Table ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Claims (
            claim_id INT PRIMARY KEY AUTO_INCREMENT,
            item_id INT NOT NULL,
            claimant_id INT NOT NULL,
            claim_status ENUM('pending', 'approved', 'rejected') NOT NULL DEFAULT 'pending',
            verification_details TEXT,
            claimed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (item_id) REFERENCES Items(item_id),
            FOREIGN KEY (claimant_id) REFERENCES Users(user_id)
        )
    """)
    
    # --- 5. Notifications Table ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Notifications (
            notification_id INT PRIMARY KEY AUTO_INCREMENT,
            user_id INT NOT NULL, 
            message TEXT NOT NULL,
            type ENUM('email', 'system') NOT NULL,
            status ENUM('sent', 'pending', 'read') NOT NULL DEFAULT 'pending',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
        )
    """)
    
    # --- Seeding (Initial Data) ---
    # Seed Categories
    try:
        categories = [('Electronics',), ('ID/Documents',), ('Apparel/Clothing',)]
        cursor.executemany("INSERT INTO Categories (name) VALUES (%s)", categories)
    except mysql.connector.Error:
        pass # Ignore if categories already exist

    # Seed Sample User
    try:
        sample_user = ('Sample User', 'sample@example.com', hash_password('password'), 'student')
        cursor.execute("INSERT INTO Users (name, email, password_hash, role) VALUES (%s, %s, %s, %s)", sample_user)
        sample_user_id = cursor.lastrowid
    except mysql.connector.Error:
        # If user exists, get the id
        cursor.execute("SELECT user_id FROM Users WHERE email = %s", ('sample@example.com',))
        result = cursor.fetchone()
        sample_user_id = result[0] if result else None

    # Seed Sample Items
    if sample_user_id:
        try:
            sample_items = [
                (sample_user_id, 1, 'Lost iPhone', 'Black iPhone 12 lost in the library', 'lost'),
                (sample_user_id, 2, 'Found Student ID', 'Student ID found near cafeteria', 'found'),
                (sample_user_id, 3, 'Lost Jacket', 'Blue jacket lost during event', 'lost'),
            ]
            cursor.executemany("INSERT INTO Items (reported_by, category_id, title, description, status) VALUES (%s, %s, %s, %s, %s)", sample_items)
        except mysql.connector.Error:
            pass # Ignore if items already exist

    db.conn.commit()
    cursor.close()
    print("✅ Database tables checked/created and seeded successfully.")
