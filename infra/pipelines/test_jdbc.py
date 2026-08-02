from pyspark.sql import SparkSession
import os

spark = (
    SparkSession.builder
    .appName("TestJDBC")
    .config(
        "spark.jars.packages",
        "com.microsoft.sqlserver:mssql-jdbc:12.4.2.jre11"
    )
    .getOrCreate()
)

jdbc_url = (
    f"jdbc:sqlserver://{os.getenv('SQL_SERVER')}:1433;"
    f"databaseName={os.getenv('SQL_DB')};"
    "encrypt=true;"
    "trustServerCertificate=false;"
    "hostNameInCertificate=*.database.windows.net;"
    "loginTimeout=30;"
)

properties = {
    "user": os.getenv("SQL_USER"),
    "password": os.getenv("SQL_PASSWORD"),
    "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver",
}

print(jdbc_url)

df = spark.read.jdbc(
    url=jdbc_url,
    table="(SELECT TOP 5 * FROM INFORMATION_SCHEMA.TABLES) t",
    properties=properties,
)

df.show()