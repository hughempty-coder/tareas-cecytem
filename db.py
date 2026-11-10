import os
import pymysql

def obtener_conexion():
    """Abre y regresa una conexión segura a Aiven usando la ruta absoluta de ca.pem."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_ca = os.path.join(base_dir, 'ca.pem')
    
    return pymysql.connect(
        host="tareas-cecytem-tareas-cecytem-bb.h.aivencloud.com",
        port=18073,
        user="avnadmin",
        password="AVNS_hQaOKr3pUXyZOLoZAG-",
        database="defaultdb",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=15,
        ssl={"ca": ruta_ca}
    )