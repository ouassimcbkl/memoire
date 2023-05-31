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
now = datetime.now()
S=now.strftime('%Y-%m-%d')
print(S)
SS=S.split()
nam="anis"
name=nam.split()
#SS=(S,nam)
dateee=input("donner la date :")
datee=dateee.split()
req = "SELECT ALL entrer.id,entrer.idemp,employer.Nomemployer FROM entrer,employer WHERE date =%s and retard ='true' and entrer.idemp = employer.id"
req3 = "SELECT ALL * FROM entrer WHERE retard ='true'"
req2 = "SELECT * FROM entrer WHERE date= %s AND idemp= %s"
#req2 = "SELECT * FROM entrer WHERE date= %s"

res=cur.execute(req,datee)
nom = cur.fetchall()
print(nom)
for item in nom:
    k = item
print(k)
SSS=(S,k)
print(SSS)
res=cur.execute(req2,SSS)
T = cur.fetchone()
print(T)