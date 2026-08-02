import random

from utils.catalogos import CIUDADES, TIPOS_ZONA


class GeneradorZonas:

    def generar(self):

        id_ciudad = random.randint(1, len(CIUDADES))

        ciudad = CIUDADES[id_ciudad]

        return (

            f"{ciudad['nombre']} - Zona {random.randint(1,999)}",

            id_ciudad,

            random.choice(ciudad["barrios"]),

            round(ciudad["lat"] + random.uniform(-0.05, 0.05), 8),

            round(ciudad["lon"] + random.uniform(-0.05, 0.05), 8),

            random.randint(1, 5),

            random.choice(TIPOS_ZONA),

            round(random.uniform(0.5, 35.0), 2)

        )

    def generar_varios(self, cantidad):

        return [self.generar() for _ in range(cantidad)]