import sys
import time
from config import get_spark_session, SILVER_PATH, GOLD_PATH
from pyspark.sql import functions as F
from pyspark.sql.window import Window

try:
    print("[1/4] Cargando módulos y configuración desde config.py...", flush=True)
    from config import get_spark_session, SILVER_PATH, GOLD_PATH
    print("      └─ Módulos y configuración cargados con éxito.", flush=True)
except Exception as e:
    print(f"\n[ERROR FATAL] Falló la carga de módulos/configuración: {e}", flush=True)
    sys.exit(1)


def build_dim_conductores(spark):
    print(" ─── [1/8] Construyendo: dim_conductores...", flush=True)
    df = spark.read.format("delta").load(f"{SILVER_PATH}/ope_conductores")
    
    dim = df.select(
        F.col("cond_id").alias("id_conductor"),
        F.concat_ws(" ", F.col("nomb_cond"), F.col("apell_cond")).alias("nombre_conductor"),
        F.col("tip_doc"),
        F.col("num_doc_hash"),
        F.col("fec_ingreso"),
        F.round(F.datediff(F.current_date(), F.col("fec_ingreso")) / 365.25, 2).alias("antiguedad_anos"),
        F.when(F.lower(F.col("tip_vehiculo")).contains("moto"), "Moto")
         .when(F.lower(F.col("tip_vehiculo")).contains("bici"), "Bicicleta")
         .when(F.lower(F.col("tip_vehiculo")).contains("van"), "Van")
         .otherwise("Camion").alias("tip_vehiculo_estandar"),
        F.col("activo").alias("es_activo"),
        F.col("calific_promedio_acum")
    ).dropDuplicates(["id_conductor"])
    
    dim.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{GOLD_PATH}/dim_conductores")
    return dim.count()


def build_dim_remitentes(spark):
    print(" ─── [2/8] Construyendo: dim_remitentes...", flush=True)
    df = spark.read.format("delta").load(f"{SILVER_PATH}/cli_remitentes")
    
    # CORRECCIÓN: Se usa razon_social en lugar de nombre_remitente
    dim = df.select(
        F.col("id_remitente"),
        F.col("razon_social").alias("nombre_remitente"),
        F.coalesce(F.col("tipo_cliente"), F.lit("Otro")).alias("segmento_industria"),
        F.coalesce(F.col("sla_entrega_horas").cast("integer"), F.lit(24)).alias("sla_entrega_horas_limpio"),
        F.col("penalidad_porc"),
        F.col("activo")
    ).dropDuplicates(["id_remitente"])
    
    dim.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{GOLD_PATH}/dim_remitentes")
    return dim.count()


def build_dim_zonas(spark):
    print(" ─── [3/8] Construyendo: dim_zonas...", flush=True)
    df_zonas = spark.read.format("delta").load(f"{SILVER_PATH}/geo_zonas")
    
    try:
        df_ciudades = spark.read.format("delta").load(f"{SILVER_PATH}/ciudades")
        df_zonas = df_zonas.join(df_ciudades, "id_ciudad", "left")
    except Exception:
        df_zonas = df_zonas.withColumn("nombre_ciudad", F.lit("Desconocido"))

    # CORRECCIÓN: Se usa id_zona en lugar de id_zona_destino
    dim = df_zonas.withColumn(
        "indice_dificultad_operativa",
        F.round(
            F.least(
                F.lit(5.0),
                F.greatest(
                    F.lit(1.0),
                    (F.coalesce(F.col("nivel_trafico_prom"), F.lit(3)) * 0.6) + 
                    ((F.coalesce(F.col("distancia_bodega_km"), F.lit(10)) / 10.0) * 0.4)
                )
            ), 2
        )
    ).select(
        F.col("id_zona").alias("id_zona"),
        F.col("nom_zona").alias("nombre_zona"),
        F.coalesce(F.col("nombre_ciudad"), F.lit("Municipio N/A")).alias("nombre_municipio"),
        F.col("distancia_bodega_km"),
        F.col("nivel_trafico_prom"),
        F.col("indice_dificultad_operativa")
    ).dropDuplicates(["id_zona"])

    dim.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{GOLD_PATH}/dim_zonas")
    return dim.count()


def build_fact_envios(spark):
    print(" ─── [4/8] Construyendo: fact_envios...", flush=True)
    df_envios = spark.read.format("delta").load(f"{SILVER_PATH}/tms_envios")
    df_remitentes = spark.read.format("delta").load(f"{SILVER_PATH}/cli_remitentes").select("id_remitente", "sla_entrega_horas")
    
    df = df_envios.join(df_remitentes, "id_remitente", "left")

    df = df.withColumn(
        "tiempo_entrega_real_horas",
        F.round((F.col("fec_entrega_real").cast("long") - F.col("fec_recepcion").cast("long")) / 3600.0, 2)
    ).withColumn(
        "horas_retraso",
        F.round((F.col("fec_entrega_real").cast("long") - F.col("fec_entrega_programada").cast("long")) / 3600.0, 2)
    ).withColumn(
        "num_intentos_realizados",
        F.when(F.col("fec_intento2").isNotNull(), 2)
         .when(F.col("fec_intento1").isNotNull(), 1)
         .otherwise(0)
    )

    fact = df.withColumn(
        "cumplimiento_sla",
        F.when(F.col("tiempo_entrega_real_horas") <= F.coalesce(F.col("sla_entrega_horas"), F.lit(24)), 1).otherwise(0)
    ).withColumn(
        "clasificacion_retraso",
        F.when(F.col("estado_final") != "Entregado", "No entregado")
         .when(F.col("horas_retraso") <= 0, "A tiempo")
         .when((F.col("horas_retraso") > 0) & (F.col("horas_retraso") <= 4), "Retraso leve")
         .when((F.col("horas_retraso") > 4) & (F.col("horas_retraso") <= 24), "Retraso moderado")
         .otherwise("Retraso critico")
    ).withColumn(
        "motivo_fallo_descripcion",
        F.coalesce(F.col("motivo_fallo_cod"), F.lit("Sin Fallo / Entregado"))
    ).withColumn("year_month", F.date_format("fec_recepcion", "yyyy-MM"))

    fact.write.format("delta").mode("overwrite").partitionBy("year_month").option("overwriteSchema", "true").save(f"{GOLD_PATH}/fact_envios")
    return fact.count()


def build_fact_rutas(spark):
    print(" ─── [5/8] Construyendo: fact_rutas...", flush=True)
    df = spark.read.format("delta").load(f"{SILVER_PATH}/gps_rutas")
    
    # CORRECCIÓN: Se calcula horas_trabajadas derivándolas de (hra_fin - hra_inicio)
    df_calc = df.withColumn(
        "horas_trabajadas_calc",
        F.round((F.col("hra_fin").cast("long") - F.col("hra_inicio").cast("long")) / 3600.0, 2)
    )

    fact = df_calc.withColumn(
        "eficiencia_ruta",
        F.round(F.coalesce(F.col("num_paradas_real"), F.lit(1)) / F.coalesce(F.col("num_paradas_plan"), F.lit(1)), 2)
    ).withColumn(
        "horas_trabajadas",
        F.greatest(F.lit(0.1), F.coalesce(F.col("horas_trabajadas_calc"), F.lit(1.0)))
    ).withColumn(
        "velocidad_promedio_kmh",
        F.round(F.col("km_recorridos") / F.col("horas_trabajadas"), 2)
    ).withColumn(
        "desviacion_porc",
        F.round((F.col("desviacion_ruta_km") / F.col("km_recorridos")) * 100, 2)
    )

    fact.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{GOLD_PATH}/fact_rutas")
    return fact.count()


def build_fact_desempeno_conductor(spark):
    print(" ─── [6/8] Construyendo: fact_desempeno_conductor...", flush=True)
    df_envios = spark.read.format("delta").load(f"{SILVER_PATH}/tms_envios")
    df_rutas = spark.read.format("delta").load(f"{SILVER_PATH}/gps_rutas")
    df_dest = spark.read.format("delta").load(f"{SILVER_PATH}/cal_destinatarios")
    
    # Unir cal_destinatarios con tms_envios para asociar cond_id
    df_dest_cond = df_dest.join(
        df_envios.select("id_envio", "cond_id"), 
        on="id_envio", 
        how="inner"
    )

    envios_kpi = df_envios.groupBy("cond_id", "fec_recepcion").agg(
        F.count("id_envio").alias("total_envios"),
        F.sum(F.when(F.col("estado_final") == "Entregado", 1).otherwise(0)).alias("envios_exitosos"),
        F.avg(F.when(F.col("fec_intento2").isNotNull(), 2).otherwise(1)).alias("intentos_promedios")
    ).withColumn("tasa_exito", F.col("envios_exitosos") / F.col("total_envios"))
    
    rutas_kpi = df_rutas.groupBy("cond_id", "fec_ruta").agg(
        F.avg("km_recorridos").alias("km_prom"),
        F.avg("desviacion_ruta_km").alias("desv_prom")
    ).withColumn("adherencia_ruta", F.greatest(F.lit(0.0), F.lit(1.0) - (F.col("desv_prom") / F.col("km_prom"))))

    dest_kpi = df_dest_cond.groupBy("cond_id").agg(F.avg("puntaje_1_5").alias("calif_prom"))
    
    # CORRECCIÓN: Se renombra fec_ruta a fec_recepcion en rutas_kpi para hacer el join por lista de columnas ["cond_id", "fec_recepcion"]
    # Esto elimina la ambigüedad de cond_id en Spark.
    rutas_kpi_renamed = rutas_kpi.withColumnRenamed("fec_ruta", "fec_recepcion")

    base = envios_kpi.join(rutas_kpi_renamed, on=["cond_id", "fec_recepcion"], how="inner") \
                     .join(dest_kpi, on="cond_id", how="left")

    fact = base.withColumn("tasa_exito_norm", F.coalesce(F.col("tasa_exito"), F.lit(0.0))) \
               .withColumn("adherencia_norm", F.coalesce(F.col("adherencia_ruta"), F.lit(0.8))) \
               .withColumn("velocidad_norm", F.lit(0.85)) \
               .withColumn("inversa_intentos_norm", F.lit(1.0) / F.coalesce(F.col("intentos_promedios"), F.lit(1.0))) \
               .withColumn("calif_norm", F.coalesce(F.col("calif_prom"), F.lit(4.0)) / 5.0) \
               .withColumn(
                    "score_desempeno",
                    F.round(
                        (F.col("tasa_exito_norm") * 0.35) + 
                        (F.col("adherencia_norm") * 0.20) + 
                        (F.col("velocidad_norm") * 0.20) + 
                        (F.col("inversa_intentos_norm") * 0.15) + 
                        (F.col("calif_norm") * 0.10), 2
                    )
               ).select(
                    F.col("cond_id").alias("id_conductor"),
                    F.col("fec_recepcion").alias("fecha"),
                    "tasa_exito",
                    "score_desempeno"
               )

    fact.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{GOLD_PATH}/fact_desempeno_conductor")
    return fact.count()

def build_fact_alertas_zona(spark):
    print(" ─── [7/8] Construyendo: fact_alertas_zona...", flush=True)
    df_envios = spark.read.format("delta").load(f"{SILVER_PATH}/tms_envios")

    diario_zona = df_envios.groupBy("id_zona_destino", "fec_recepcion").agg(
        F.count("id_envio").alias("total_envios"),
        F.sum(F.when(F.col("estado_final") != "Entregado", 1).otherwise(0)).alias("total_fallos")
    ).withColumn("tasa_fallo_actual", F.col("total_fallos") / F.col("total_envios"))

    w_window = Window.partitionBy("id_zona_destino").orderBy("fec_recepcion").rowsBetween(-28, -1)
    
    alertas = diario_zona.withColumn("promedio_historico_4w", F.avg("tasa_fallo_actual").over(w_window)) \
                         .withColumn("desviacion_porc", ((F.col("tasa_fallo_actual") - F.col("promedio_historico_4w")) / F.col("promedio_historico_4w")) * 100) \
                         .filter(F.col("desviacion_porc") > 25) \
                         .select(
                             F.col("id_zona_destino").alias("id_zona"),
                             F.col("fec_recepcion").alias("fecha"),
                             F.round("tasa_fallo_actual", 4).alias("tasa_actual"),
                             F.round("promedio_historico_4w", 4).alias("promedio_historico"),
                             F.round("desviacion_porc", 2).alias("porcentaje_desviacion")
                         )

    alertas.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{GOLD_PATH}/fact_alertas_zona")
    return alertas.count()


def build_kpi_executive_dashboard(spark):
    print(" ─── [8/8] Construyendo: kpi_executive_dashboard...", flush=True)
    df_envios = spark.read.format("delta").load(f"{SILVER_PATH}/tms_envios")
    df_nov = spark.read.format("delta").load(f"{SILVER_PATH}/dir_novedades")

    df_envios.createOrReplaceTempView("v_envios")
    df_nov.createOrReplaceTempView("v_novedades")

    kpi = spark.sql("""
        SELECT 
            CURRENT_DATE() as fecha_reporte,
            COUNT(DISTINCT e.id_envio) as total_envios_procesados,
            SUM(e.vr_declarado) as total_valor_declarado,
            AVG(e.vr_declarado) as ticket_promedio,
            SUM(e.peso_kg) as volumen_total_kg,
            COUNT(DISTINCT e.cond_id) as conductores_activos,
            COUNT(DISTINCT n.id_novedad) as total_novedades
        FROM v_envios e
        LEFT JOIN v_novedades n ON e.id_envio = n.id_envio
    """)

    kpi.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{GOLD_PATH}/kpi_executive_dashboard")
    return kpi.count()


def main():
    print("\n==================================================", flush=True)
    print("  INICIANDO TRANSFORMACIÓN GOLD: MODELO DIMENSIONAL ", flush=True)
    print("==================================================\n", flush=True)

    print("[2/4] Inicializando SparkSession...", flush=True)
    start_time_global = time.time()
    
    try:
        spark = get_spark_session(app_name="03_Gold_Dimensional_Pipeline")
        print("      └─ SparkSession creada exitosamente.\n", flush=True)
    except Exception as e:
        print(f"\n[ERROR FATAL] No se pudo crear la SparkSession: {e}", flush=True)
        sys.exit(1)

    pipeline = [
        ("Dim Conductores", build_dim_conductores),
        ("Dim Remitentes", build_dim_remitentes),
        ("Dim Zonas", build_dim_zonas),
        ("Fact Envíos", build_fact_envios),
        ("Fact Rutas", build_fact_rutas),
        ("Fact Desempeño Conductor", build_fact_desempeno_conductor),
        ("Fact Alertas Zona", build_fact_alertas_zona),
        ("KPI Executive Dashboard", build_kpi_executive_dashboard)
    ]
    
    print(f"[3/4] Procesando {len(pipeline)} tablas hacia ADLS Gen2 (Gold)...", flush=True)
    print(f"      Ruta destino base: {GOLD_PATH}\n", flush=True)

    success_count = 0
    error_count = 0

    for idx, (name, func) in enumerate(pipeline, 1):
        start_time_step = time.time()
        try:
            records = func(spark)
            elapsed = round(time.time() - start_time_step, 2)
            print(f"  [OK] {name} procesado con éxito ({records} registros - {elapsed}s)\n", flush=True)
            success_count += 1
        except Exception as e:
            elapsed = round(time.time() - start_time_step, 2)
            print(f"  [ERROR] Falló el procesamiento de '{name}' ({elapsed}s):", flush=True)
            print(f"          {e}\n", flush=True)
            error_count += 1

    total_time = round(time.time() - start_time_global, 2)
    
    print("[4/4] Finalizando Pipeline Gold...", flush=True)
    spark.stop()

    print("==================================================", flush=True)
    print("  RESUMEN DE EJECUCIÓN - CAPA GOLD               ", flush=True)
    print("==================================================", flush=True)
    print(f"  • Tiempo total   : {total_time} segundos", flush=True)
    print(f"  • Exitosas       : {success_count}/{len(pipeline)}", flush=True)
    print(f"  • Con error      : {error_count}/{len(pipeline)}", flush=True)
    print("==================================================\n", flush=True)

if __name__ == "__main__":
    main()