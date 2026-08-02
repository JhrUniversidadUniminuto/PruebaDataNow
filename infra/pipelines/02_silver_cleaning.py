from config import get_spark_session, BRONZE_PATH, SILVER_PATH
from pyspark.sql import functions as F

spark = get_spark_session("Silver_Layer_Processing")

def save_to_silver(df, table_name):
    """Guarda un DataFrame limpio en la capa Silver."""
    df.write \
        .format("delta") \
        .mode("overwrite") \
        .option("overwriteSchema", "true") \
        .save(f"{SILVER_PATH}/{table_name}")
    print(f"✅ [{table_name.upper()}] Procesada y guardada en Silver ({df.count()} registros).")

def save_to_errors(df, table_name):
    """Guarda registros descartados en la tabla de errores."""
    if df.count() > 0:
        df.write \
            .format("delta") \
            .mode("append") \
            .option("mergeSchema", "true") \
            .save(f"{SILVER_PATH}/_errors_{table_name}")
        print(f"⚠️ [{table_name.upper()}] Se enviaron {df.count()} registros a _errors_{table_name}.")

# =========================================================================
# 1. CIUDADES
# =========================================================================
def clean_ciudades():
    print("\n--- Procesando CIUDADES ---")
    df = spark.read.format("delta").load(f"{BRONZE_PATH}/ciudades").dropDuplicates()
    df_clean = df.withColumn("nombre_ciudad", F.upper(F.trim(F.col("nombre_ciudad"))))
    save_to_silver(df_clean, "ciudades")

# =========================================================================
# 2. OPE_CONDUCTORES
# =========================================================================
def clean_conductores():
    print("\n--- Procesando OPE_CONDUCTORES ---")
    df = spark.read.format("delta").load(f"{BRONZE_PATH}/ope_conductores").dropDuplicates()
    df_clean = (
        df
        .withColumn("fec_ingreso", F.to_date(F.col("fec_ingreso")))
        .withColumn("calific_promedio_acum", F.col("calific_promedio_acum").cast("decimal(3,2)"))
        .withColumn("activo", F.col("activo").cast("boolean"))
    )
    save_to_silver(df_clean, "ope_conductores")

# =========================================================================
# 3. CLI_REMITENTES
# =========================================================================
def clean_remitentes():
    print("\n--- Procesando CLI_REMITENTES ---")
    df = spark.read.format("delta").load(f"{BRONZE_PATH}/cli_remitentes").dropDuplicates()
    df_clean = (
        df
        .withColumn("penalidad_porc", F.col("penalidad_porc").cast("decimal(5,2)"))
        .withColumn("sla_entrega_horas", F.col("sla_entrega_horas").cast("integer"))
        .withColumn("activo", F.col("activo").cast("boolean"))
    )
    save_to_silver(df_clean, "cli_remitentes")

# =========================================================================
# 4. GEO_ZONAS
# =========================================================================
def clean_geo_zonas():
    print("\n--- Procesando GEO_ZONAS ---")
    df = spark.read.format("delta").load(f"{BRONZE_PATH}/geo_zonas").dropDuplicates()
    df_clean = (
        df
        .withColumn("latitud_centroide", F.col("latitud_centroide").cast("decimal(10,8)"))
        .withColumn("longitud_centroide", F.col("longitud_centroide").cast("decimal(11,8)"))
        .withColumn("distancia_bodega_km", F.col("distancia_bodega_km").cast("decimal(8,2)"))
    )
    save_to_silver(df_clean, "geo_zonas")

# =========================================================================
# 5. GPS_RUTAS
# =========================================================================
def clean_gps_rutas():
    print("\n--- Procesando GPS_RUTAS ---")
    df = spark.read.format("delta").load(f"{BRONZE_PATH}/gps_rutas").dropDuplicates()
    df_clean = (
        df
        .withColumn("fec_ruta", F.to_date(F.col("fec_ruta")))
        .withColumn("km_recorridos", F.col("km_recorridos").cast("decimal(10,2)"))
        .withColumn("desviacion_ruta_km", F.col("desviacion_ruta_km").cast("decimal(10,2)"))
        .withColumn("consumo_combustible", F.col("consumo_combustible").cast("decimal(10,2)"))
    )
    save_to_silver(df_clean, "gps_rutas")

# =========================================================================
# 6. CAL_DESTINATARIOS
# =========================================================================
def clean_cal_destinatarios():
    print("\n--- Procesando CAL_DESTINATARIOS ---")
    df = spark.read.format("delta").load(f"{BRONZE_PATH}/cal_destinatarios").dropDuplicates()
    df_clean = (
        df
        .withColumn("fec_calificacion", F.to_timestamp(F.col("fec_calificacion")))
        .withColumn("puntaje_1_5", F.col("puntaje_1_5").cast("integer"))
    )
    save_to_silver(df_clean, "cal_destinatarios")

# =========================================================================
# 7. DIR_NOVEDADES
# =========================================================================
def clean_dir_novedades():
    print("\n--- Procesando DIR_NOVEDADES ---")
    df = spark.read.format("delta").load(f"{BRONZE_PATH}/dir_novedades").dropDuplicates()
    df_clean = (
        df
        .withColumn("fec_novedad", F.to_timestamp(F.col("fec_novedad")))
        .withColumn("requiere_accion", F.col("requiere_accion").cast("boolean"))
    )
    save_to_silver(df_clean, "dir_novedades")

# =========================================================================
# 8. TMS_ENVIOS (Con Reglas de Calidad e Integridad)
# =========================================================================
def clean_tms_envios():
    print("\n--- Procesando TMS_ENVIOS ---")
    df_envios = spark.read.format("delta").load(f"{BRONZE_PATH}/tms_envios")
    
    # Intento de lectura de dimensiones en Silver para FK
    try:
        df_conductores = spark.read.format("delta").load(f"{SILVER_PATH}/ope_conductores")
        df_remitentes = spark.read.format("delta").load(f"{SILVER_PATH}/cli_remitentes")
    except Exception:
        df_conductores, df_remitentes = None, None

    total_inicial = df_envios.count()

    df_processed = (
        df_envios
        .withColumn("peso_kg", F.col("peso_kg").cast("decimal(8,2)"))
        .withColumn("vr_declarado", F.col("vr_declarado").cast("decimal(12,2)"))
        .withColumn("fec_recepcion", F.to_date(F.col("fec_recepcion")))
        .withColumn("fec_entrega_programada", F.to_timestamp(F.col("fec_entrega_programada")))
        .withColumn("fec_entrega_real", F.to_timestamp(F.col("fec_entrega_real")))
        .withColumn("estado_final", F.coalesce(F.col("estado_final"), F.lit("SIN_ESTADO")))
        .withColumn("es_nulo_motivo_fallo", F.when(F.col("motivo_fallo_cod").isNull(), 1).otherwise(0))
    )

    df_dedup = df_processed.dropDuplicates()

    # Validaciones Not Null
    cond_nulos = (
        F.col("id_envio").isNull() | 
        F.col("id_remitente").isNull() | 
        F.col("cond_id").isNull() | 
        F.col("id_zona_destino").isNull() | 
        F.col("fec_recepcion").isNull() | 
        F.col("vr_declarado").isNull()
    )

    df_bad_nulls = df_dedup.filter(cond_nulos).withColumn("motivo_error", F.lit("CAMPO_OBLIGATORIO_NULO"))
    df_candidates = df_dedup.filter(~cond_nulos)

    # Validaciones FK
    if df_conductores is not None:
        df_fk_cond_err = df_candidates.join(df_conductores.select("cond_id"), on="cond_id", how="left_anti").withColumn("motivo_error", F.lit("FK_CONDUCTOR_NO_EXISTE"))
        df_candidates = df_candidates.join(df_conductores.select("cond_id"), on="cond_id", how="inner")
    else:
        df_fk_cond_err = spark.createDataFrame([], df_candidates.schema).withColumn("motivo_error", F.lit(""))

    if df_remitentes is not None:
        df_fk_rem_err = df_candidates.join(df_remitentes.select("id_remitente"), on="id_remitente", how="left_anti").withColumn("motivo_error", F.lit("FK_REMITENTE_NO_EXISTE"))
        df_silver_clean = df_candidates.join(df_remitentes.select("id_remitente"), on="id_remitente", how="inner")
    else:
        df_fk_rem_err = spark.createDataFrame([], df_candidates.schema).withColumn("motivo_error", F.lit(""))
        df_silver_clean = df_candidates

    df_errors = df_bad_nulls.unionByName(df_fk_cond_err, allowMissingColumns=True).unionByName(df_fk_rem_err, allowMissingColumns=True)

    save_to_silver(df_silver_clean, "tms_envios")
    save_to_errors(df_errors, "tms_envios")

# =========================================================================
# EJECUCIÓN DEL PIPELINE
# =========================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("    INICIANDO PROCESAMIENTO GENERAL DE LA CAPA SILVER")
    print("=" * 60)
    
    clean_ciudades()
    clean_conductores()
    clean_remitentes()
    clean_geo_zonas()
    clean_gps_rutas()
    clean_cal_destinatarios()
    clean_dir_novedades()
    clean_tms_envios()
    
    print("\n" + "=" * 60)
    print("   ¡TODAS LAS TABLAS FUERON MIGRADAS A SILVER EXITOSAMENTE! 🎉")
    print("=" * 60)