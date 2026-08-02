from generators.geo_zonas import GeneradorZonas
from repositories.geo_zonas_repository import GeoZonasRepository

from generators.conductores import GeneradorConductores
from repositories.conductores_repository import ConductoresRepository

from generators.remitentes import GeneradorRemitentes
from repositories.remitentes_repository import RemitentesRepository

from generators.gps_rutas import GeneradorRutas
from repositories.gps_rutas_repository import RutasRepository

from generators.tms_envios import GeneradorEnvios
from repositories.tms_envios_repository import EnviosRepository

from generators.novedades import GeneradorNovedades
from repositories.novedades_repository import NovedadesRepository

from generators.cal_destinatarios import GeneradorCalificaciones
from repositories.cal_destinatarios_repository import CalificacionesRepository

from config.parametros import *


class Pipeline:

    def cargar_zonas(self):
        print("\n========================================")
        print("Generando zonas...")
        datos = GeneradorZonas().generar_varios(NUM_ZONAS)
        GeoZonasRepository().guardar(datos)
        print("✅ Zonas cargadas correctamente")

    def cargar_conductores(self):
        print("\n========================================")
        print("Generando conductores...")
        datos = GeneradorConductores().generar_varios(NUM_CONDUCTORES)
        ConductoresRepository().guardar(datos)
        print("✅ Conductores cargados correctamente")

    def cargar_remitentes(self):
        print("\n========================================")
        print("Generando remitentes...")
        datos = GeneradorRemitentes().generar_varios(NUM_REMITENTES)
        RemitentesRepository().guardar(datos)
        print("✅ Remitente cargados correctamente")

    def cargar_rutas(self):

        print("\n========================================")
        print("Generando rutas...")
        datos = GeneradorRutas().generar_varios(NUM_RUTAS)
        RutasRepository().guardar(datos)
        print("✅ Rutas cargadas correctamente")     

    def cargar_envios(self):

        print("\n========================================")
        print("Generando envíos...")

        generador = GeneradorEnvios()

        repo = EnviosRepository()

        repo.abrir()

        batch = 1000

        restantes = NUM_ENVIOS

        cargados = 0

        while restantes > 0:

            cantidad = min(batch, restantes)

            datos = generador.generar_varios(cantidad)

            repo.guardar(datos)

            cargados += cantidad

            restantes -= cantidad

            if cargados % 100000 == 0 or cargados == NUM_ENVIOS:

                print(f"✅ Insertados {cargados:,} de {NUM_ENVIOS:,}")

        repo.cerrar()

        print("\n========================================")
        print("✅ Envíos cargados correctamente")

    def cargar_novedades(self):

            print("\n========================================")
            print("Generando novedades...")

            generador = GeneradorNovedades()

            repo = NovedadesRepository()

            cantidad_total = repo.contar_envios_con_novedad()


            print(f"Se encontraron {cantidad_total:,} envíos con novedad.")

            repo.abrir()

            batch = 1000

            restantes = cantidad_total

            cargados = 0

            while restantes > 0:

                cantidad = min(batch, restantes)

                datos = generador.generar_varios(cantidad)

                repo.guardar(datos)

                cargados += cantidad

                restantes -= cantidad

                if cargados % 50000 == 0 or cargados == cantidad_total:

                    print(f"✅ Insertados {cargados:,} de {cantidad_total:,}")

            repo.cerrar()

            print("\n========================================")
            print("✅ Novedades cargadas correctamente")

    def cargar_calificaciones(self):

        print("\n========================================")
        print("Generando calificaciones...")

        generador = GeneradorCalificaciones()

        repo = CalificacionesRepository()

        cantidad_total = repo.contar_envios_entregados()

        print(f"Se encontraron {cantidad_total:,} envíos entregados.")

        repo.abrir()

        batch = 10000

        restantes = cantidad_total

        cargados = 0

        while restantes > 0:

            cantidad = min(batch, restantes)

            datos = generador.generar_varios(cantidad)

            repo.guardar(datos)

            cargados += cantidad

            restantes -= cantidad

            if cargados % 50000 == 0 or cargados == cantidad_total:

                print(f"✅ Insertados {cargados:,} de {cantidad_total:,}")

        repo.cerrar()

        print("\n========================================")
        print("✅ Calificaciones cargadas correctamente")            

    def ejecutar(self):
        self.cargar_zonas()
        self.cargar_conductores()
        self.cargar_remitentes()
        self.cargar_rutas()
        self.cargar_envios()
        self.cargar_novedades()
        self.cargar_calificaciones()

        print("\n========================================")
        print("Pipeline ejecutado correctamente.")