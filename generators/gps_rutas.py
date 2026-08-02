import random
from datetime import datetime, timedelta

from config.parametros import NUM_CONDUCTORES


class GeneradorRutas:

    def generar(self):

        hora_inicio = random.randint(5, 9)

        minuto_inicio = random.randint(0, 59)

        inicio = datetime(2026, 1, 1, hora_inicio, minuto_inicio)

        duracion = random.randint(6, 12)

        fin = inicio + timedelta(hours=duracion)

        km = round(random.uniform(60, 350), 2)

        plan = random.randint(15, 60)

        real = max(0, plan + random.randint(-5, 8))

        return (

            random.randint(1, NUM_CONDUCTORES),

            inicio.date(),

            inicio.time(),

            fin.time(),

            km,

            plan,

            real,

            round(random.uniform(0, 20), 2),

            round(km / random.uniform(8, 18), 2)

        )

    def generar_varios(self, cantidad):

        return [

            self.generar()

            for _ in range(cantidad)

        ]