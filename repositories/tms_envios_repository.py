import time

from config.conexion import get_connection


class EnviosRepository:

    SQL_INSERT = """
    INSERT INTO TMS_ENVIOS(
        id_remitente,
        cond_id,
        id_zona_destino,
        tip_paquete,
        peso_kg,
        fec_recepcion,
        hra_recepcion,
        fec_entrega_programada,
        fec_intento1,
        hra_intento1,
        resultado_intento1,
        fec_intento2,
        hra_intento2,
        resultado_intento2,
        fec_entrega_real,
        estado_final,
        motivo_fallo_cod,
        vr_declarado
    )
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """

    def abrir(self):

        self.conexion = get_connection()

        self.cursor = self.conexion.cursor()

        self.cursor.fast_executemany = True

    def guardar(self, datos):

        inicio = time.time()

        print(f"\nIniciando inserción de {len(datos):,} registros...")

        self.cursor.executemany(

            self.SQL_INSERT,

            datos

        )

        print(f"Executemany terminó en {time.time() - inicio:.2f} segundos")

        inicio = time.time()

        self.conexion.commit()

        print(f"Commit terminó en {time.time() - inicio:.2f} segundos")

    def cerrar(self):

        self.conexion.close()

    def obtener_conductores(self):

        conexion = get_connection()

        cursor = conexion.cursor()

        cursor.execute("SELECT cond_id FROM OPE_CONDUCTORES WHERE activo=1")

        datos = [x[0] for x in cursor.fetchall()]

        conexion.close()

        return datos


    def obtener_remitentes(self):

        conexion = get_connection()

        cursor = conexion.cursor()

        cursor.execute("SELECT id_remitente FROM CLI_REMITENTES WHERE activo=1")

        datos = [x[0] for x in cursor.fetchall()]

        conexion.close()

        return datos


    def obtener_zonas(self):

        conexion = get_connection()

        cursor = conexion.cursor()

        cursor.execute("SELECT id_zona FROM GEO_ZONAS")

        datos = [x[0] for x in cursor.fetchall()]

        conexion.close()

        return datos