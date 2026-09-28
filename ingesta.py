import boto3
import mysql.connector
import csv

host_name = "172.31.81.224"   #IP privada mv bd
port_number = "8005"
user_name = "root"
password_db = "utec"
database_name = "bd_api_employees"
tabla = "employees"

ficheroUpload = "data.csv"
nombreBucket = "vab-output-01"


mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name,
                               password=password_db, database=database_name)
cursor = mydb.cursor()
cursor.execute("SELECT * FROM " + tabla)
columnas = [col[0] for col in cursor.description]
registros = cursor.fetchall()
cursor.close()
mydb.close()
print("Registros leidos:", len(registros))


with open(ficheroUpload, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(columnas)
    writer.writerows(registros)

s3 = boto3.client('s3')
response = s3.upload_file(ficheroUpload, nombreBucket, ficheroUpload)
print(response)

print("Ingesta completada")
