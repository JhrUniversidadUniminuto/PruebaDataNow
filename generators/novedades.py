import random

from datetime import datetime, timedelta

from repositories.novedades_repository import NovedadesRepository


MAPEO_NOVEDADES = {

    "CLI_AUS": (

        "Cliente Ausente",

        "El cliente no se encontraba en la dirección registrada."

    ),

    "DIR_ERR": (

        "Dirección Incorrecta",

        "La dirección suministrada es incorrecta."

    ),

    "RECHAZO": (

        "Rechazo del Cliente",

        "El cliente rechazó recibir el envío."

    ),

    "SIN_ACCESO": (

        "Zona sin Acceso",

        "No fue posible acceder al destino."

    )

}


class GeneradorNovedades:

    def __init__(self):

        repo = NovedadesRepository()

        self.envios = repo.obtener_envios_con_novedad()

        random.shuffle(self.envios)


    def generar(self):

        if len(self.envios) == 0:

            raise Exception("No hay más envíos disponibles para generar novedades.")

        id_envio, estado, motivo = self.envios.pop()

        fecha = datetime.now() - timedelta(

            days=random.randint(0,365)

        )

        tipo, descripcion = MAPEO_NOVEDADES.get(

            motivo,

            (

                "Otra Novedad",

                "Se registró una novedad durante el proceso."

            )

        )

        agente = random.randint(1,500)

        requiere_accion = random.choice([0,1])

        return (

            id_envio,

            fecha,

            tipo,

            descripcion,

            agente,

            requiere_accion

        )

    def generar_varios(self, cantidad):

        cantidad = min(cantidad, len(self.envios))

        return [

            self.generar()

            for _ in range(cantidad)

        ]