import sqlite3

connection = sqlite3.connect('device.db')

with open('schema_device.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO devices (mac_address, hostname, original_line) VALUES (?, ?, ?)", 
	('aaccff662277', 'rdepta0061', 'aa:cc:ff:66:22:77;rdepta0061;demo example from scma') 
	)

connection.commit()
connection.close()
