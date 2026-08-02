import time

inicio = time.time()

datos = generador.generar_varios(cantidad)

print(f"Generación: {time.time() - inicio:.2f} segundos")

inicio = time.time()

repo.guardar(datos)

print(f"Inserción: {time.time() - inicio:.2f} segundos")