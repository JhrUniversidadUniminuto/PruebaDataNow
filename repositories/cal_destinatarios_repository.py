from config.conexion import get_connection


class CalificacionesRepository:

    SQL_INSERT = """

    INSERT INTO CAL_DESTINATARIOS(

        id_envio,
        fec_calificacion,
        puntaje_1_5,
        comentario_texto,
        canal_calificacion

    )

    VALUES(?,?,?,?,?)

    """

    def abrir(self):

        self.conexion = get_connection()

        self.cursor = self.conexion.cursor()

        self.cursor.fast_executemany = True


    def guardar(self, datos):

        self.cursor.executemany(

            self.SQL_INSERT,

            datos

        )

        self.conexion.commit()


    def cerrar(self):

        self.conexion.close()


    def obtener_envios_entregados(self):

        conexion = get_connection()

        cursor = conexion.cursor()

        cursor.execute("""

            SELECT id_envio

            FROM TMS_ENVIOS

            WHERE estado_final='Entregado'

        """)

        datos = cursor.fetchall()

        conexion.close()

        return datos


    def contar_envios_entregados(self):

        conexion = get_connection()

        cursor = conexion.cursor()

        cursor.execute("""

            SELECT COUNT(*)

            FROM TMS_ENVIOS

            WHERE estado_final='Entregado'

        """)

        cantidad = cursor.fetchone()[0]

        conexion.close()

        return cantidad