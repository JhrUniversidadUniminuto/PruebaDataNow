from config.conexion import get_connection


class GeoZonasRepository:

    SQL = """

    INSERT INTO GEO_ZONAS(

        nom_zona ,
        id_ciudad,
        barrio_referencia,
        latitud_centroide,
        longitud_centroide,
        nivel_trafico_prom,
        tip_zona,
        distancia_bodega_km

    )

    VALUES(?,?,?,?,?,?,?,?)

    """

    def guardar(self,datos):

        conexion = get_connection()

        cursor = conexion.cursor()

        cursor.fast_executemany = True

        cursor.executemany(

            self.SQL,

            datos

        )

        conexion.commit()

        conexion.close()