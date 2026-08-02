import random

from datetime import datetime, timedelta

from repositories.tms_envios_repository import EnviosRepository


TIPOS_PAQUETE = {

    "Documento": 0.30,
    "Sobre": 0.15,
    "Caja": 0.35,
    "Electrónico": 0.10,
    "Fragil": 0.10

}

ESTADOS = {

    "Entregado": 0.88,
    "En Transito": 0.05,
    "Devuelto": 0.04,
    "Cancelado": 0.03

}

RESULTADOS = [

    "Entregado",
    "Cliente Ausente",
    "Dirección Incorrecta",
    "Rechazado"

]

MOTIVOS = [

    None,
    "CLI_AUS",
    "DIR_ERR",
    "RECHAZO",
    "SIN_ACCESO"

]


class GeneradorEnvios:

    def __init__(self):

        repo = EnviosRepository()

        self.conductores = repo.obtener_conductores()

        self.remitentes = repo.obtener_remitentes()

        self.zonas = repo.obtener_zonas()


    def generar(self):

        id_remitente = random.choice(self.remitentes)

        cond_id = random.choice(self.conductores)

        id_zona = random.choice(self.zonas)


        tipo_paquete = random.choices(

            population=list(TIPOS_PAQUETE.keys()),
            weights=list(TIPOS_PAQUETE.values()),
            k=1

        )[0]


        peso = round(random.uniform(0.20,40),2)


        fecha_recepcion = datetime.now() - timedelta(

            days=random.randint(0,365)

        )


        hora_recepcion = fecha_recepcion.time()


        fecha_programada = fecha_recepcion + timedelta(

            days=random.randint(1,3)

        )


        estado = random.choices(

            population=list(ESTADOS.keys()),
            weights=list(ESTADOS.values()),
            k=1

        )[0]


        fecha_intento1 = fecha_programada

        hora_intento1 = fecha_programada.time()


        fecha_intento2 = None

        hora_intento2 = None

        resultado2 = None

        fecha_real = None

        motivo = None


        if estado == "Entregado":

            resultado1 = "Entregado"

            fecha_real = fecha_programada + timedelta(

                hours=random.randint(0,6)

            )


        elif estado == "En Transito":

            resultado1 = "En Ruta"


        elif estado == "Cancelado":

            resultado1 = "Cancelado"

            motivo = random.choice([

                "CLI_AUS",

                "RECHAZO",

                "DIR_ERR"

            ])


        else:

            resultado1 = random.choice([

                "Cliente Ausente",

                "Dirección Incorrecta"

            ])

            fecha_intento2 = fecha_programada + timedelta(days=1)

            hora_intento2 = fecha_programada.time()

            resultado2 = "Devuelto"

            motivo = "CLI_AUS"


        valor = round(

            random.uniform(50000,5000000),

            2

        )


        return (

            id_remitente,

            cond_id,

            id_zona,

            tipo_paquete,

            peso,

            fecha_recepcion.date(),

            hora_recepcion,

            fecha_programada.date(),

            fecha_intento1.date(),

            hora_intento1,

            resultado1,

            fecha_intento2.date() if fecha_intento2 else None,

            hora_intento2,

            resultado2,

            fecha_real.date() if fecha_real else None,

            estado,

            motivo,

            valor

        )


    def generar_varios(self,cantidad):

        return [

            self.generar()

            for _ in range(cantidad)

        ]