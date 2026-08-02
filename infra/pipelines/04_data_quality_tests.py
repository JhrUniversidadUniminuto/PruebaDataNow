# pipelines/04_data_quality_tests.py
from config import get_spark_session, SILVER_PATH, GOLD_PATH
from pyspark.sql import functions as F

def run_quality_tests():
    spark = get_spark_session(app_name="04_Data_Quality_Tests")
    passed_tests = 0
    total_tests = 5
    
    print("\n==================================================")
    print("--- EJECUTANDO PRUEBAS DE CALIDAD DE DATOS (LOGÍSTICA) ---")
    print("==================================================\n")
    
    # Cargar DataFrames de prueba
    df_silver_envios = spark.read.format("delta").load(f"{SILVER_PATH}/tms_envios")
    df_silver_cond = spark.read.format("delta").load(f"{SILVER_PATH}/ope_conductores")
    df_gold_kpi = spark.read.format("delta").load(f"{GOLD_PATH}/kpi_executive_dashboard")
    df_gold_perf = spark.read.format("delta").load(f"{GOLD_PATH}/fact_desempeno_conductor")
    
    # Test 1: No deben existir id_envio nulos en Silver (Integridad Referencial)
    null_envio = df_silver_envios.filter(F.col("id_envio").isNull()).count()
    if null_envio == 0:
        print("✅ Test 1 PASÓ: No hay id_envio nulos en Silver.")
        passed_tests += 1
    else:
        print(f"❌ Test 1 FALLÓ: Se encontraron {null_envio} nulos en id_envio.")

    # Test 2: Unicidad de Claves Primarias en Silver
    duplicates = df_silver_envios.groupBy("id_envio").count().filter("count > 1").count()
    if duplicates == 0:
        print("✅ Test 2 PASÓ: No hay duplicados en id_envio (Clave Primaria única).")
        passed_tests += 1
    else:
        print(f"❌ Test 2 FALLÓ: Existen {duplicates} envíos duplicados.")

    # Test 3: Anonimización de Datos Sensibles (PII) en Silver (num_doc debió ser hasheado)
    cond_cols = df_silver_cond.columns
    if "num_doc_hash" in cond_cols and "num_doc" not in cond_cols:
        print("✅ Test 3 PASÓ: Información PII (Documentos) hasheada/enmascarada correctamente en Silver.")
        passed_tests += 1
    else:
        print("❌ Test 3 FALLÓ: Se detectó número de documento en texto plano o falta el hash.")

    # Test 4: La tabla Gold de KPIs Ejecutivos debe contener datos
    if df_gold_kpi.count() > 0:
        print("✅ Test 4 PASÓ: La tabla de KPIs Ejecutivos (kpi_executive_dashboard) contiene datos.")
        passed_tests += 1
    else:
        print("❌ Test 4 FALLÓ: Tabla de KPIs Ejecutivos vacía.")

    # Test 5: Regla de Negocio en Gold (El score de desempeño debe estar entre 0.0 y 1.0)
    invalid_scores = df_gold_perf.filter((F.col("score_desempeno") < 0.0) | (F.col("score_desempeno") > 1.0)).count()
    if invalid_scores == 0:
        print("✅ Test 5 PASÓ: Todos los scores de desempeño en Gold están en el rango válido [0.0, 1.0].")
        passed_tests += 1
    else:
        print(f"❌ Test 5 FALLÓ: Se encontraron {invalid_scores} registros con score fuera de rango.")

    print("==================================================")
    print(f"RESULTADO FINAL: {passed_tests}/{total_tests} Pruebas aprobadas.")
    print("==================================================\n")

if __name__ == "__main__":
    run_quality_tests()