import mysql.connector

mydb = mysql.connector.connect(
    host = "211.55.39.22",
    user = "knu",
    passwd = "Knu_0987!@#",

    port = "43306",
)
print(mydb)