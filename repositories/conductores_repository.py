from config.conexion import get_connection


class ConductoresRepository:

    SQL = """

    INSERT INTO OPE_CONDUCTORES(

        nomb_cond,
        apell_cond,
        tip_doc,
        num_doc_hash,
        fec_ingreso,
        id_ciudad_base,
        tip_vehiculo,
        cod_zona_asignada,
        activo,
        calific_promedio_acum

    )

    VALUES(?,?,?,?,?,?,?,?,?,?)

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