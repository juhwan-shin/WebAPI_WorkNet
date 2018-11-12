import mysql.connector

mydb = mysql.connector.connect(
    host = "xxx.xx.xx.xx",
    user = "xxx",
    passwd = "xxxxxxxx",

    port = "xxxxx",
)
print(mydb)