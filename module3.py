from tokenize import String
import mysql.connector
from datetime import datetime


db = mysql.connector.connect(
  host = "localhost",
  user = "root",
  password = "anis1234",
  database='firstp'
)
cur = db.cursor()
n="anis-abed"
req1="SELECT * FROM employer WHERE Nomemployer= %s"
name=n.split()
res=cur.execute(req1,name)
nom = cur.fetchone()
nomm=nom[0]
print('nom:  '+nom[0]+'\nchemin:  '+nom[1])

