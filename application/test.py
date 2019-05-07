import psycopg2

conn = psycopg2.connect(dbname='coursework_db', user='cw_user',
                        password='bogdan10', host='localhost', port=5432)

cursor = conn.cursor()

cursor.execute('SELECT login FROM application_userinfo')
passw = cursor.fetchall()

print(passw[0][0])

print(type(passw[0][0]))


