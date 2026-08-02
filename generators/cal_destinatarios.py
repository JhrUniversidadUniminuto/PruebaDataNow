import random

from datetime import datetime, timedelta

from repositories.cal_destinatarios_repository import CalificacionesRepository


CANALES=[

    "App",

    "Correo",

    "SMS",

    "Web"

]


COMENTARIOS={

    5:[
        "Excelente servicio.",
        "Entrega muy rápida.",
        "Todo perfecto."
    ],

    4:[
        "Buen servicio.",
        "Llegó a tiempo."
    ],

    3:[
        "Servicio aceptable.",
        "Puede mejorar."
    ],

    2:[
        "Llegó tarde.",
        "No cumplió expectativas."
    ],

    1:[
        "Muy mal servicio.",
        "No volvería a usarlo."
    ]

}


class GeneradorCalificaciones:

    def __init__(self):

        repo = CalificacionesRepository()

        self.envios = repo.obtener_envios_entregados()

        random.shuffle(self.envios)


    def generar(self):

        id_envio = self.envios.pop()[0]

        puntaje = random.choices(

            population=[5,4,3,2,1],

            weights=[60,20,10,7,3],

            k=1

        )[0]

        comentario = random.choice(

            COMENTARIOS[puntaje]

        )

        fecha = datetime.now()-timedelta(

            days=random.randint(0,365)

        )

        canal = random.choice(CANALES)

        return(

            id_envio,

            fecha,

            puntaje,

            comentario,

            canal

        )


    def generar_varios(self,cantidad):

        cantidad=min(

            cantidad,

            len(self.envios)

        )

        return[

            self.generar()

            for _ in range(cantidad)

        ]