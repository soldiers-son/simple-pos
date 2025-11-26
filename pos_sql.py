import sqlite3

conn = sqlite3.connect('pos.db')
c = conn.cursor()

# c.execute("""CREATE TABLE inventory (
#              item string,
#              quantity string,
#              price float
#             )""")

# c.execute (""" CREATE TABLE IF NOT EXISTS sales (
#            item string,
#            quantity int,
#            price float,
#            date DATE
#            )""")

conn.commit()
print('Data entry successful')
conn.close()
