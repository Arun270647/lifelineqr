"""
One-time script: drop old admins table (username column) and recreate
with email column, then seed default admin credentials.
"""
import mysql.connector

passwords = ['', 'sjssjs', 'root', 'mysql', 'password']
conn = None

for pwd in passwords:
    try:
        conn = mysql.connector.connect(
            host='localhost', user='root', password=pwd, database='lifelineqr'
        )
        print(f"Connected (password={repr(pwd)})")
        break
    except Exception:
        pass

if not conn:
    print("ERROR: Could not connect to MySQL with any known password.")
    exit(1)

cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS admins")
print("Dropped old admins table.")

cur.execute("""
    CREATE TABLE admins (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")
print("Created new admins table with email column.")

cur.execute(
    "INSERT INTO admins (email, password) VALUES (%s, %s)",
    ('admin@lifelineqr.com', 'admin@123')
)
conn.commit()
print("Default admin seeded.")
print()
print("  Email   : admin@lifelineqr.com")
print("  Password: admin@123")
print()
print("Done! You can now log in from the main login page.")

cur.close()
conn.close()
