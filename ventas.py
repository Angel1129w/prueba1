import cgi
import cx_Oracle

def procesar_venta():
    try:
        # Obtener los datos del formulario
        form = cgi.FieldStorage()

        cliente_nombre = form.getvalue('nombre')
        cliente_telefono = form.getvalue('telefono')
        cliente_direccion = form.getvalue('direccion')

        # Recoger múltiples productos
        tipos_huevo = form.getlist('tipo_huevo[]')
        cantidades_cubetas = list(map(int, form.getlist('cantidad_cubetas[]')))
        cantidades_unidades = list(map(int, form.getlist('cantidad_unidades[]')))

        # Conectar con Oracle
        dsn = cx_Oracle.makedsn("191.107.183.75", 1521, service_name="XE")
        conexion = cx_Oracle.connect(user="C##ANGEL", password="M423i32R4", dsn=dsn)
        cursor = conexion.cursor()

        # Precios por unidad y cubeta
        precios_unidad = {
            "HUEVO BLANCO A": 417, "HUEVO BLANCO AA": 450, "HUEVO BLANCO B": 367, "HUEVO BLANCO EXTRA": 533,
            "HUEVO ROJO A": 417, "HUEVO ROJO AA": 450, "HUEVO ROJO B": 367, "HUEVO ROJO EXTRA": 533
        }
        precios_cubeta = {
            "HUEVO BLANCO A": 12500, "HUEVO BLANCO AA": 13500, "HUEVO BLANCO B": 11000, "HUEVO BLANCO EXTRA": 16000,
            "HUEVO ROJO A": 12500, "HUEVO ROJO AA": 13500, "HUEVO ROJO B": 11000, "HUEVO ROJO EXTRA": 16000
        }

        valor_total = 0

        for tipo, cubetas, unidades in zip(tipos_huevo, cantidades_cubetas, cantidades_unidades):
            # Calcular el valor total
            valor_total += (cubetas * precios_cubeta[tipo]) + (unidades * precios_unidad[tipo])

            # Actualizar inventario
            cantidad_total = (cubetas * 30) + unidades
            cursor.execute("""
                UPDATE huevos
                SET cantidad = cantidad - :cantidad
                WHERE tipo_huevo = :tipo_huevo
            """, {"cantidad": cantidad_total, "tipo_huevo": tipo})

            # Insertar venta
            cursor.execute("""
                INSERT INTO ventas_huevos (id, cliente_nombre, cliente_telefono, cliente_direccion, tipo_huevo, cantidad_cubetas, cantidad_unidades, valor_total)
                VALUES (ventas_huevos_seq.NEXTVAL, :nombre, :telefono, :direccion, :tipo_huevo, :cantidad_cubetas, :cantidad_unidades, :valor_total)
            """, {
                "nombre": cliente_nombre,
                "telefono": cliente_telefono,
                "direccion": cliente_direccion,
                "tipo_huevo": tipo,
                "cantidad_cubetas": cubetas,
                "cantidad_unidades": unidades,
                "valor_total": valor_total
            })

        conexion.commit()

        print("Content-Type: text/html\n")
        print("<h1>Venta registrada con éxito. Valor total: ${}</h1>".format(valor_total))

    except Exception as e:
        print("Content-Type: text/html\n")
        print("<h1>Error al procesar la venta: {}</h1>".format(e))

    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

procesar_venta()
