import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="anis1234",
  database="firstp"
)
cur = db.cursor()

query = "SELECT * FROM employer WHERE id NOT IN ( SELECT idemp FROM entrer WHERE date >= CURDATE() - INTERVAL 1 MONTH AND date <= CURDATE() )"


cur.execute(query)
result = cur.fetchall()

print("Employés absents au cours du dernier mois: ")
for row in result:
    print(row)

cur.close()
db.close()

