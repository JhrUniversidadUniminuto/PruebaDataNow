import os
import sys
from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession

# Resolucion dinamica del ejecutable de Python activo (evita fallos de 'python3' en Windows/Linux)
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable


STORAGE_ACCOUNT = os.getenv("AZURE_STORAGE_ACCOUNT", "stpruebasdatanowdev")
STORAGE_KEY = os.getenv("AZURE_STORAGE_KEY")

BRONZE_PATH = f"abfss://bronze@{STORAGE_ACCOUNT}.dfs.core.windows.net"
SILVER_PATH = f"abfss://silver@{STORAGE_ACCOUNT}.dfs.core.windows.net"
GOLD_PATH = f"abfss://gold@{STORAGE_ACCOUNT}.dfs.core.windows.net"


SQL_SERVER = os.getenv(
    "SQL_SERVER", "logitrackjulian2026pruebadatanow.database.windows.net"
)
SQL_DB = os.getenv("SQL_DB", "LogiTrack_Transaccional")
SQL_USER = os.getenv("SQL_USER", "rootadmin")
SQL_PASSWORD = os.getenv("SQL_PASSWORD", "admin123*")

JDBC_URL = f"jdbc:sqlserver://{SQL_SERVER}:1433;databaseName={SQL_DB};encrypt=true;trustServerCertificate=false;"
JDBC_PROPS = {
    "user": SQL_USER,
    "password": SQL_PASSWORD,
    "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver",
}


def get_spark_session(app_name="DataNow_Medallion_Pipeline"):
    packages = [
        "org.apache.hadoop:hadoop-azure:3.3.4",
        "com.microsoft.sqlserver:mssql-jdbc:12.6.1.jre11",
    ]

    builder = (
        SparkSession.builder.appName(app_name)
        .config("spark.log.level", "ERROR")
        .config("spark.pyspark.python", sys.executable)
        .config("spark.pyspark.driver.python", sys.executable)
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config(f"fs.azure.account.key.{STORAGE_ACCOUNT}.dfs.core.windows.net", STORAGE_KEY)
        .config("spark.shutdown.hook.reorder", "false")
    )

    spark = configure_spark_with_delta_pip(builder, extra_packages=packages).getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")

    return spark