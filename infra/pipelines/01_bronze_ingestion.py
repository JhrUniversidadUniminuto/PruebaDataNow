import sys
import time

print("\n==================================================", flush=True)
print("  INICIANDO PIPELINE DE INGESTIÓN: CAPA BRONZE    ", flush=True)
print("==================================================\n", flush=True)


try:
    print("[1/4] Cargando módulos y configuración desde config.py...", flush=True)
    from config import (
        get_spark_session,
        JDBC_URL,
        SQL_USER,
        SQL_PASSWORD,
        BRONZE_PATH
    )
    from pyspark.sql.functions import current_timestamp, lit
    print("      └─ Módulos y configuración cargados con éxito.", flush=True)
except Exception as e:
    print(f"\n[ERROR FATAL] Falló la carga de módulos/configuración: {e}", flush=True)
    sys.exit(1)


TABLES_TO_INGEST = [
    "OPE_CONDUCTORES",
    "CIUDADES",
    "GEO_ZONAS",
    "CLI_REMITENTES",
    "GPS_RUTAS",
    "TMS_ENVIOS",
    "DIR_NOVEDADES",
    "CAL_DESTINATARIOS"
]


def main():
    print("[2/4] Inicializando SparkSession (Delta Lake + Azure Storage)...", flush=True)
    start_time_global = time.time()
    
    try:
        spark = get_spark_session(app_name="01_Bronze_Ingestion")
        print("      └─ SparkSession creada exitosamente.", flush=True)
    except Exception as e:
        print(f"\n[ERROR FATAL] No se pudo crear la SparkSession: {e}", flush=True)
        sys.exit(1)

    print(f"\n[3/4] Procesando {len(TABLES_TO_INGEST)} tablas hacia ADLS Gen2 (Bronze)...", flush=True)
    print(f"      Ruta destino base: {BRONZE_PATH}\n", flush=True)

    success_count = 0
    error_count = 0


    for idx, table_name in enumerate(TABLES_TO_INGEST, 1):
        print(f"------------ [{idx}/{len(TABLES_TO_INGEST)}] Tabla: {table_name} ------------", flush=True)
        start_time_table = time.time()
        
        try:

            print("  [1/3] Leyendo desde Azure SQL...", flush=True)
            df_raw = (
                spark.read.format("jdbc")
                .option("url", JDBC_URL)
                .option("dbtable", table_name)
                .option("user", SQL_USER)
                .option("password", SQL_PASSWORD)
                .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver")
                .load()
            )


            print("  [2/3] Inyectando campos de auditoría...", flush=True)
            df_bronze = (
                df_raw
                .withColumn("_ingested_at", current_timestamp())
                .withColumn("_source_table", lit(table_name))
            )


            target_path = f"{BRONZE_PATH}/{table_name.lower()}"
            print(f"  [3/3] Guardando formato Delta en: {target_path}", flush=True)
            
            (
                df_bronze.write
                .format("delta")
                .mode("overwrite")
                .option("mergeSchema", "true")
                .save(target_path)
            )

            elapsed_table = round(time.time() - start_time_table, 2)
            print(f"  [OK] Tabla '{table_name}' procesada con éxito ({elapsed_table}s)\n", flush=True)
            success_count += 1

        except Exception as e:
            elapsed_table = round(time.time() - start_time_table, 2)
            print(f"  [ERROR] Falló el procesamiento de '{table_name}' ({elapsed_table}s):", flush=True)
            print(f"          {e}\n", flush=True)
            error_count += 1


    total_time = round(time.time() - start_time_global, 2)
    print("==================================================", flush=True)
    print("  RESUMEN DE EJECUCIÓN - CAPA BRONZE               ", flush=True)
    print("==================================================", flush=True)
    print(f"  • Tiempo total   : {total_time} segundos", flush=True)
    print(f"  • Exitosas       : {success_count}/{len(TABLES_TO_INGEST)}", flush=True)
    print(f"  • Con error      : {error_count}/{len(TABLES_TO_INGEST)}", flush=True)
    print("==================================================\n", flush=True)

    spark.stop()

if __name__ == "__main__":
    main()