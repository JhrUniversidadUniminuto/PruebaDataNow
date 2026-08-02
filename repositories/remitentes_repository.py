from config.conexion import get_connection


class RemitentesRepository:

    SQL = """
    INSERT INTO CLI_REMITENTES
    (
        razon_social,
        tipo_cliente,
        ciudad_principal,
        sla_entrega_horas,
        penalidad_porc,
        activo
    )
    VALUES (?,?,?,?,?,?)
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