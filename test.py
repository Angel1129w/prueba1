import cx_Oracle

try:
    # Datos de conexión
    dsn = cx_Oracle.makedsn("localhost", 1521, service_name="XE")
    conexion = cx_Oracle.connect(user="C##ANGEL", password="M423i32R4", dsn=dsn)

    print("✅ Conexión exitosa a Oracle.")
    conexion.close()

except cx_Oracle.Error as error:
    print("❌ Error al conectar a Oracle:", error)
