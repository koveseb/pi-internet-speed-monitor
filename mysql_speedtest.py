import config
import re
import time
import subprocess
import mysql.connector

mydb = mysql.connector.connect(
    host=config.host, database=config.database, user=config.user, password=config.password
)

response = (
    subprocess.Popen("/usr/local/bin/speedtest-cli --simple", shell=True, stdout=subprocess.PIPE)
    .stdout.read()
    .decode("utf-8")
)
ping = re.findall("Ping:\s(.*?)\s", response, re.MULTILINE)
download = re.findall("Download:\s(.*?)\s", response, re.MULTILINE)
upload = re.findall("Upload:\s(.*?)\s", response, re.MULTILINE)

ping = ping[0].replace(",", ".")
download = download[0].replace(",", ".")
upload = upload[0].replace(",", ".")

mycursor = mydb.cursor()

sql = "INSERT INTO customers (ping, download, upload) VALUES (%s, %s, %s)"
val = (float(ping), float(download), float(upload))
mycursor.execute(sql, val)
mydb.commit()
print(mycursor.rowcount, "record inserted.")
