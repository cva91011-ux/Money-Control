import sqlite3
from datetime import datetime



conexion = sqlite3.connect("money.db")
cursor = conexion.cursor()


# Tabla de saldos

cursor.execute("""
CREATE TABLE IF NOT EXISTS saldo(
    id INTEGER PRIMARY KEY,
    fisico REAL,
    digital REAL
)
""")


# Tabla historial

cursor.execute("""
CREATE TABLE IF NOT EXISTS historial(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT,
    hora TEXT,
    motivo TEXT,
    categoria TEXT,
    monto REAL,
    moneda TEXT,
    movimiento TEXT
)
""")


# Crear saldo inicial

cursor.execute(
    "SELECT * FROM saldo"
)

if cursor.fetchone() is None:

    cursor.execute(
        "INSERT INTO saldo VALUES(1,0,0)"
    )


conexion.commit()



def obtener_saldo():

    cursor.execute(
        "SELECT fisico,digital FROM saldo WHERE id=1"
    )

    return cursor.fetchone()



def cambiar_saldo(fisico,digital):

    cursor.execute(
        """
        UPDATE saldo
        SET fisico=?,digital=?
        WHERE id=1
        """,
        (fisico,digital)
    )

    conexion.commit()



def guardar_movimiento(
    motivo,
    categoria,
    monto,
    moneda,
    movimiento
):

    ahora=datetime.now()

    cursor.execute(
        """
        INSERT INTO historial
        (fecha,hora,motivo,categoria,monto,moneda,movimiento)
        VALUES(?,?,?,?,?,?,?)
        """,
        (
        ahora.strftime("%d/%m/%Y"),
        ahora.strftime("%H:%M"),
        motivo,
        categoria,
        monto,
        moneda,
        movimiento
        )
    )

    conexion.commit()



def obtener_historial():

    cursor.execute(
        """
        SELECT * FROM historial
        ORDER BY id DESC
        """
    )

    return cursor.fetchall()
    
def crear_patron():

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS seguridad(
        id INTEGER PRIMARY KEY,
        patron TEXT
    )
    """)

    cursor.execute(
        "SELECT * FROM seguridad"
    )

    if cursor.fetchone() is None:

        cursor.execute(
            "INSERT INTO seguridad VALUES(1,'1234')"
        )

    conexion.commit()



crear_patron()



def obtener_patron():

    cursor.execute(
        "SELECT patron FROM seguridad WHERE id=1"
    )

    return cursor.fetchone()[0]



def cambiar_patron(nuevo):

    cursor.execute(
        """
        UPDATE seguridad
        SET patron=?
        WHERE id=1
        """,
        (nuevo,)
    )

    conexion.commit()
    
def crear_configuracion():

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS configuracion(
        id INTEGER PRIMARY KEY,
        fondo TEXT
    )
    """)

    cursor.execute(
        "SELECT * FROM configuracion"
    )

    if cursor.fetchone() is None:

        cursor.execute(
    "INSERT INTO configuracion VALUES(1,'')"
)
       

    conexion.commit()



crear_configuracion()



def obtener_fondo():

    cursor.execute(
        "SELECT fondo FROM configuracion WHERE id=1"
    )

    return cursor.fetchone()[0]



def guardar_fondo(ruta):

    cursor.execute(
        """
        UPDATE configuracion
        SET fondo=?
        WHERE id=1
        """,
        (ruta,)
    )

    conexion.commit()
    
    def obtener_gastos_categoria():

    	cursor.execute("""
  		  SELECT categoria, SUM(monto)
    		FROM historial
    		WHERE movimiento='Retiro'
   		 GROUP BY categoria
    """)

    return cursor.fetchall()