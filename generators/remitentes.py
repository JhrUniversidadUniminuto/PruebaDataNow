import random

from faker import Faker

from utils.catalogos import (
    CIUDADES,
    TIPOS_CLIENTE,
    EMPRESAS
)

fake = Faker("es_CO")


class GeneradorRemitentes:

    def generar(self):

        id_ciudad = random.randint(1, len(CIUDADES))

        tipo_cliente = random.choices(

            population=list(TIPOS_CLIENTE.keys()),
            weights=list(TIPOS_CLIENTE.values()),
            k=1

        )[0]

        return (

            random.choice(EMPRESAS),

            tipo_cliente,

            id_ciudad,

            random.choice([4, 8, 12, 24, 48, 72]),

            round(random.uniform(0, 15), 2),

            random.choices(

                [1, 0],

                weights=[95, 5],

                k=1

            )[0]

        )

    def generar_varios(self, cantidad):

        return [

            self.generar()

            for _ in range(cantidad)

        ]