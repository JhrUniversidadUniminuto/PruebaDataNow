from config.conexion import get_connection


class RutasRepository:

    SQL = """

    INSERT INTO GPS_RUTAS(

        cond_id,

        fec_ruta,

        hra_inicio,

        hra_fin,

        km_recorridos,

        num_paradas_plan,

        num_paradas_real,

        desviacion_ruta_km,

        consumo_combustible

    )

    VALUES(?,?,?,?,?,?,?,?,?)

    """

    def guardar(self, datos):

        conexion = get_connection()

        cursor = conexion.cursor()

        cursor.fast_executemany = True

        cursor.executemany(

            self.SQL,

            datos

        )

        conexion.commit()

        conexion.close()