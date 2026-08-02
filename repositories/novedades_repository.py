from config.conexion import get_connection


class NovedadesRepository:

    SQL_INSERT = """

    INSERT INTO DIR_NOVEDADES(

        id_envio,
        fec_novedad,
        tip_novedad,
        desc_novedad,
        id_agente_registro,
        requiere_accion

    )

    VALUES(?,?,?,?,?,?)

    """

    def abrir(self):

        self.conexion = get_connection()

        self.cursor = self.conexion.cursor()

        self.cursor.fast_executemany = True


    def guardar(self,datos):

        self.cursor.executemany(

            self.SQL_INSERT,

            datos

        )

        self.conexion.commit()


    def cerrar(self):

        self.conexion.close()


    def obtener_envios_con_novedad(self):

        conexion = get_connection()

        cursor = conexion.cursor()

        cursor.execute("""

            SELECT
                id_envio,
                estado_final,
                motivo_fallo_cod

            FROM TMS_ENVIOS

            WHERE motivo_fallo_cod IS NOT NULL

        """)

        datos = cursor.fetchall()

        conexion.close()

        return datos

    def contar_envios_con_novedad(self):

        conexion = get_connection()

        cursor = conexion.cursor()

        cursor.execute("""

            SELECT COUNT(*)

            FROM TMS_ENVIOS

            WHERE motivo_fallo_cod IS NOT NULL

        """)

        cantidad = cursor.fetchone()[0]

        conexion.close()

        return cantidad