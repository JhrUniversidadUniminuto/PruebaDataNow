import random

from faker import Faker

from utils.catalogos import *
from utils.hash import generar_hash
from utils.probabilidades import elegir

fake = Faker("es_CO")


class GeneradorConductores:

    def generar(self):

        documento = random.randint(
            10000000,
            99999999
        )

        ciudad = random.randint(
            1,
            10
        )

        return (

            fake.first_name(),

            fake.last_name(),

            random.choice(TIPOS_DOCUMENTO),

            generar_hash(documento),

            fake.date_between(
                "-10y",
                "today"
            ),

            ciudad,

            elegir(TIPOS_VEHICULO),

            random.randint(
                1,
                300
            ),

            random.random() < 0.95,

            round(
                random.uniform(3.5,5),
                2
            )

        )

    def generar_varios(self,cantidad):

        return [

            self.generar()

            for _ in range(cantidad)

        ]