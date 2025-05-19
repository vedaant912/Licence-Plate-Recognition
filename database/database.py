import sqlite3

def check_plate_info(plate_number):

    conn = sqlite3.connect('plates.db')
    cursor = conn.cursor()

    cursor.execute('SELECT owner_name, has_fine, fine_amount FROM license_plates WHERE plate_number = ?', (plate_number,))
    row = cursor.fetchone()
    conn.close()

    if row:

        return {
            'owner_name': row[0],
            'has_fine': bool(row[1]),
            'fine_amount': row[2]
        }
    
    return None