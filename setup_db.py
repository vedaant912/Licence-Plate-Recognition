import sqlite3

conn = sqlite3.connect('plates.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS license_plates (
            plate_number TEXT PRIMARY KEY,
            owner_name TEXT,
            has_fine INTEGER,
            fine_amount INTEGER              
    )
""")

cursor.execute("INSERT OR IGNORE INTO license_plates VALUES (?, ?, ?, ?)", ("AB123CD", "John Doe", 1, 75))
cursor.execute("INSERT OR IGNORE INTO license_plates VALUES (?, ?, ?, ?)", ("XY456ZT", "Alice Smith", 0, 0))

conn.commit()
conn.close()