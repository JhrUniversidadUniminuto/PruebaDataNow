import random

def elegir(diccionario):

    return random.choices(

        population=list(diccionario.keys()),
        weights=list(diccionario.values()),
        k=1

    )[0]