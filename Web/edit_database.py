import sqlite3
from werkzeug.security import generate_password_hash
connection=sqlite3.connect('SQLite.db',check_same_thread=False)
cursor=connection.cursor()



cursor.execute('INSERT INTO user VALUES (?,?,?)',(1,'Popamaster415', generate_password_hash('popamain415', method='pbkdf2:sha256')))

cursor.execute('UPDATE post SET author_id=1;')

connection.commit()
connection.close()