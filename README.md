# 📋 Resultados y Evidencias - Prueba Técnica

## 📑 Contenido

- 📸 Evidencias Creación cuenta Cloud
- 📄 Documentación

---

<details>
<summary>📸 <strong>Ver evidencias</strong></summary>

<br>

<table>
<tr>
<td width="50%">

### ☁️ Evidencia 1

**Creación de presupuestos en Microsoft Azure**

Se evidencia la cuenta creada en Azure.

</td>

<td width="50%" align="center">

<img src="img/CuentaCreadaAzure.png" width="450">

</td>
</tr>
<tr>
<td width="50%">

### ☁️ Evidencia 2

**Crédito Gratuito**

Se evidencia la configuración del presupuesto realizada en Azure.

</td>

<td width="50%" align="center">

<img src="img/ImgPresupuestos.png" width="450">

</td>
</tr>
<tr>
<td width="50%">

### ☁️ Evidencia 3

**Alerta de presupuesto configurada con limite de USD 10 y notificación por correo**

Se evidencia la configuración de alertas a presupuesto.

</td>

<td width="50%" align="center">

<img src="img/AlertaPresupuesto.png" width="450">

</td>
</tr>
<tr>
<td width="50%">

### ☁️ Evidencia 4

**método de pago verificado y funcional, incluso si el saldo disponible es mínimo**

Se evidencia los métodos de pago que están asociados.

</td>

<td width="50%" align="center">

<img src="img/metodopago.png" width="450">

</td>
</tr>
<tr>
<td width="50%">

### ☁️ Evidencia 5

**autenticación de doble factor activada en la cuenta cloud para protección de la cuenta**

Se evidencia inicio sección con doble factor.
</td>

<td width="50%" align="center">

<img src="img/SeccionDobleFactor.png" width="450">

</td>
</tr>
<tr>
<td width="50%">

### ☁️ Evidencia 6

**Region de trabajo seleccionada: East US para Azure y AWS, us-central1 para GCP**

Se evidencia región donde esta creados los recursos.
</td>

<td width="50%" align="center">

<img src="img/RegionAzure.png" width="450">

</td>
</tr>
<tr>
<td width="50%">

### ☁️ Evidencia 7

**Correo electrónico y numero de teléfono verificados en el portal de la plataforma**

Se evidencia el correo electrónico verificado.
</td>

<td width="50%" align="center">

<img src="img/ContactoVerificadoAzure.png" width="450">

</td>
</tr>

<tr>
<td width="50%">

### ☁️ Evidencia 8

**Beneficios de correo estudiantil activados si el candidato dispone de correo institucional**

Se evidencia los beneficios de la cuenta estudiantil.
</td>

<td width="50%" align="center">

<img src="img/suscripcion.png" width="450">

</td>
</tr>
<tr>
<td width="50%">

### ☁️ Evidencia 9

**Repositorio Git creado en GitHub, GitLab o Bitbucket con acceso compartido al evaluador**

Se evidencia repositorio Git Creado.
</td>

<td width="50%" align="center">

<img src="img/GitPublico.png" width="450">

</td>
</tr>
<tr>
<td width="50%">

### ☁️ Evidencia 10

**Herramienta de IaC instalada localmente: Terraform, Bicep, AWS CLI o gcloud CLI según la plataforma**

Se evidencia localmente instalado el Azure Cli.
</td>

<td width="50%" align="center">

<img src="img/CliAzureLocal.png" width="450">

</td>
</tr>
<tr>
<td width="50%">

### ☁️ Evidencia 11

**CLI de la plataforma cloud instalado y autenticado correctamente en el equipo local**

Se evidencia localmente ejecutándose el Azure Cli.
</td>

<td width="50%" align="center">

<img src="img/CliAutenticadoCorrectamente.png" width="450">

</td>
</tr>
<tr>
<td width="50%">

### ☁️ Evidencia 12

**Acceso probado a la consola o portal de la plataforma desde el navegador y desde el terminal**

Se evidencia localmente ejecutándose el Azure Cli y el portal web de Azure.
</td>

<td width="50%" align="center">

<img src="img/PruebaAzureTerminal.png" width="450">
<br>
<img src="img/PortalWebAzure.png" width="450">
</td>
</tr>
</table>

</details>

---

<details>
<summary>📄 <strong>Ver documentación</strong></summary>

<br>

<h1>🚚 DOCUMENTACIÓN TÉCNICA Y ENTREGABLE FINAL</h1>
<p><strong>Empresa:</strong> LogiTrack S.A.S. (Logística y Cadena de Suministro)</p>
<p><strong>Plataforma Cloud:</strong> Microsoft Azure</p>
<p><strong>Arquitectura:</strong> Medallón (Bronze, Silver, Gold) sobre Azure Data Lake Storage Gen2 (ADLS Gen2)</p>

<hr>

<h2>💡 1. Justificación del Escenario y Plataforma</h2>
<ul>
    <li><strong>Sector Seleccionado:</strong> Escenario D - Logística y Cadena de Suministro (LogiTrack S.A.S.).
        <ul>
            <li><em>Justificación:</em> Permite resolver la problemática de la alta tasa de entregas fallidas (14.3%) mediante la consolidación de más de 2 millones de envíos y datos de telemetría GPS. Permite calcular un <em>Score de Desempeño Multidimensional</em> justo para conductores y detectar alertas de retrasos en zonas críticas.</li>
        </ul>
    </li>
    <li><strong>Plataforma Cloud:</strong> Microsoft Azure.
        <ul>
            <li><em>Justificación:</em> Proporciona una suite nativa para soluciones de Big Data y analítica enterprise mediante ADLS Gen2, Azure Data Factory y Azure Key Vault para la protección de secretos.</li>
        </ul>
    </li>
</ul>

<hr>

<h2>🏗️ 2. Entregable Fase 1: ENTREGABLE FASE 1 — GENERACION DE DATOS Y MODELO RELACIONAL</h2>

<h3>2.1 Script de generación de datos dummy</h3>

<p>
El código fuente de la generación de datos sintéticos se encuentra en el siguiente repositorio:
</p>

<ul>
  <li>
    <strong>Pipeline principal:</strong>
    <a href="https://github.com/JhrUniversidadUniminuto/PruebaDataNow/blob/main/main.py">main.py</a>
  </li>
  <li>
    <strong>Orquestación:</strong>
    <a href="https://github.com/JhrUniversidadUniminuto/PruebaDataNow/blob/main/pipeline.py">pipeline.py</a>
  </li>
  <li>
    <strong>Configuración (semilla aleatoria y parámetros):</strong>
    <a href="https://github.com/JhrUniversidadUniminuto/PruebaDataNow/blob/main/config/parametros.py">config/parametros.py</a>
  </li>
  <li>
    <strong>Generadores de datos:</strong>
    <a href="https://github.com/JhrUniversidadUniminuto/PruebaDataNow/tree/main/generators">Carpeta generators</a>
  </li>
  <br>
  <br>
  <li>
    <strong>Evidencia Desencadenador datos sintéticos por perspectiva:</strong>
    <img src="img/DesencadenadorDatosSinteticos.png" width="450">
  </li>
    
</ul>

<h3>2.2 Script SQL o Python de carga en la base de datos relacional seleccionada</h3>
  <li>
    <strong>Script creacion de modelo de datos transaccional:</strong>
    <a href="https://github.com/JhrUniversidadUniminuto/PruebaDataNow/tree/main/CreacionModeloTrascionalAzure.txt">Script</a>
  </li>

<h3>2.3 Diagrama Entidad-Relación (ER) de todas las tablas generadas, ubicado en la carpeta /docs del repositorio</h3>
  <li>
    <strong>Diagrama</strong>
    <img src="img/Er.png" width="450">
  </li>
<h3>2.4 Evidencia de la carga exitosa: captura de pantalla o resultado de SELECT COUNT(*) por tabla</h3>
  <li>
    <strong>OPE_CONDUCTORES</strong>
    <img src="img/cargaOPE_CONDUCTORES.png" width="450">
  </li>
  <li>
    <strong>Ciudades</strong>
    <img src="img/CargaCiudad.png" width="450">
  </li>
  <li>
    <strong>GeoZonas</strong>
    <img src="img/GeoZonas.png" width="450">
  </li>
  <li>
    <strong>Remitentes</strong>
    <img src="img/CargaClientes.png" width="450">
  </li>
  <li>
    <strong>Gps Rutas</strong>
    <img src="img/Cargarutas.png" width="450">
  </li>
  <li>
    <strong>Tms Envios</strong>
    <img src="img/Cargatmfenvios.png" width="450">
  </li>
  <li>
    <strong>Novedades</strong>
    <img src="img/CargaNovedad.png" width="450">
  </li>
  <li>
    <strong>Destinatarios</strong>
    <img src="img/Cargardestinatarios.png" width="450">
  </li>
<hr>

<h2>🏗️ 3. ENTREGABLE FASE 2 — INFRAESTRUCTURA COMO CODIGO</h2>
<h3>3.1 Código IaC completo en la carpeta /infra del repositorio, con README de instrucciones de despliegue</h3>

<p>
README:
</p>
<ul>
  <li>
    <strong>Configuiración:</strong>
    <a href="https://github.com/JhrUniversidadUniminuto/PruebaDataNow/blob/main/03CREACIONMODELObroncesilvergold.txt">Leerme</a>
  </li>
    
</ul>
<h3>3.2 Evidencia del despliegue exitoso: captura de pantalla del portal o salida del terminal con el resultado del apply</h3>

<p>
Imagen evidencia:
</p>
<ul>
  <li>
    <strong>Evidencia:</strong>
    <img src="img/TerraformaIniciado.png" width="450">
    <img src="img/TerraformAplicado.png" width="450">
  </li>
    
</ul>
<h3>3.3 Lista de recursos creados con sus nombres, regiones y propósito dentro de la solución</h3>

<p>
La siguiente tabla resume los recursos desplegados en Microsoft Azure mediante Infraestructura como Código (IaC). Se indica el nombre de cada recurso, su tipo, la región donde fue aprovisionado y el papel que desempeña dentro de la arquitectura implementada.
</p>

<p align="center">
<img src="img/RecursosCreadosAzure.png" width="900">
</p>

<br>
<p align="center">
<img src="img/RecursosCreadosAzure.png" width="900">
</p>

| Recurso | Tipo | Región | Propósito dentro de la solución |
|----------|------|--------|---------------------------------|
| **PruebasDataNow** | Resource Group | East US | Contenedor lógico que agrupa todos los recursos de Azure utilizados por la solución para facilitar su administración, monitoreo y eliminación. |
| **stpruebasdatanowdev** | Storage Account (ADLS Gen2) | East US | Repositorio principal del Data Lake donde se almacenan las capas Bronze, Silver y Gold con archivos Parquet generados por el pipeline. |
| **adf-pruebasdatanow-dev** | Azure Data Factory V2 | East US | Orquesta la ejecución de los procesos ETL/ELT, coordinando la ingestión y transformación de datos. |
| **kv-pruebasdatanow-dev** | Azure Key Vault | East US | Almacena de forma segura secretos, credenciales y cadenas de conexión utilizadas por los diferentes servicios. |
| **log-pruebasdatanow-dev** | Log Analytics Workspace | East US | Centraliza registros, métricas y diagnósticos para facilitar el monitoreo y la solución de incidentes. |
| **ag-pruebasdatanow-dev** | Action Group | Global | Gestiona el envío de alertas y notificaciones cuando se presentan eventos críticos o fallos en la solución. |
| **logitrackjulian2026PruebaDataNow** | Azure SQL Server | Central US | Servidor lógico que hospeda la base de datos transaccional utilizada como origen de información. |
| **LogiTrack_Transaccional** | Azure SQL Database | Central US | Base de datos OLTP donde se almacenan conductores, envíos, rutas GPS, remitentes, novedades, zonas y demás información operacional. |
<hr>

<h2>🏅 4. Entregable Fase 3: Pipeline End-to-End (Arquitectura Medallón)</h2>

<h3>4.1 Capas del Pipeline</h3>
<ul>
    <li><strong>Capa Bronze (<code>01_bronze_ingestion.py</code>):</strong> Ingesta cruda incremental en Parquet/Delta con metadatos de auditoría (<code>_ingestion_timestamp</code>, <code>_source_system</code>, <code>_batch_id</code>) y particionamiento por fecha (<code>año/mes/día</code>).</li>
    <li><strong>Capa Silver (<code>02_silver_transformation.py</code>):</strong> Limpieza de nulos corrompidos, eliminación de duplicados, deduplicación y enmascaramiento con <strong>Hash SHA-256</strong> para PII (<code>num_doc_hash</code>). Los registros erróneos se canalizan a <code>silver_error_records</code>[cite: 1].</li>
    <li><strong>Capa Gold (<code>03_gold_transformation.py</code>):</strong> Construcción del modelo en estrella (Star Schema) aplicando reglas de negocio.</li>
</ul>

<h3>4.2 Documentación de Linaje de Datos (Data Lineage)</h3>
<table border="1" cellspacing="0" cellpadding="5">
    <thead>
        <tr>
            <th>Campo Calculado (Gold)</th>
            <th>Tabla Destino</th>
            <th>Tabla(s) Origen (Silver)</th>
            <th>Transformación / Regla de Negocio Aplicada</th>
            <th>Propósito Analítico</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong><code>score_desempeno</code></strong></td>
            <td><code>fact_desempeno_conductor</code></td>
            <td><code>tms_envios</code><br><code>gps_rutas</code><br><code>cal_destinatarios</code></td>
            <td>Promedio ponderado normalizado (0.0 a 1.0):<br><code>(tasa_exito * 0.35) + (adherencia_ruta * 0.20) + (velocidad_norm * 0.20) + (inversa_intentos * 0.15) + (calific_norm * 0.10)</code>[cite: 1]</td>
            <td>Asignación justa de bonos basada en desempeño multidimensional[cite: 1].</td>
        </tr>
        <tr>
            <td><strong><code>clasificacion_retraso</code></strong></td>
            <td><code>fact_envios</code></td>
            <td><code>tms_envios</code></td>
            <td>Diferencia en horas entre <code>fec_entrega_real</code> y <code>fec_entrega_programada</code>[cite: 1].<br>• <code>&lt;=0h</code>: A tiempo<br>• <code>1-4h</code>: Retraso leve<br>• <code>4-24h</code>: Retraso moderado<br>• <code>&gt;24h</code>: Retraso crítico[cite: 1]</td>
            <td>Cuantificar penalizaciones de SLA e identificar cuellos de botella[cite: 1].</td>
        </tr>
        <tr>
            <td><strong><code>alerta_desviacion</code></strong></td>
            <td><code>fact_alertas_zona</code></td>
            <td><code>tms_envios</code><br><code>geo_zonas</code></td>
            <td>Compara la tasa de fallo actual vs el promedio de las últimas 4 semanas. Se activa si supera en <strong>&gt;25%</strong> la media histórica[cite: 1].</td>
            <td>Distinguir fallos estructurales de la zona vs fallos del conductor[cite: 1].</td>
        </tr>
    </tbody>
</table>

<h3>4.3 Pruebas Automatizadas de Calidad de Datos</h3>
<ol>
    <li><strong>Integridad Referencial:</strong> Claves primarias no nulas en <code>fact_envios</code>.</li>
    <li><strong>Unicidad:</strong> Cero registros duplicados en <code>dim_conductores</code>.</li>
    <li><strong>Anonimización PII:</strong> Formato Hash SHA-256 validado en <code>num_doc_hash</code>.</li>
    <li><strong>Rangos Válidos:</strong> <code>score_desempeno</code> restringido estrictamente entre <code>0.0</code> y <code>1.0</code>[cite: 1].</li>
    <li><strong>No Vacío:</strong> Verificación de registros poblados en <code>kpi_executive_dashboard</code>.</li>
</ol>

<hr>

<h2>⚙️ 5. Entregable Fase 4: Orquestación del Pipeline</h2>
<ul>
    <li><strong>DAG de Orquestación:</strong> <code>orchestration/dag_datanow_pipeline.py</code>.</li>
    <li><strong>Programación (CRON):</strong> Diaria a las <strong>02:00 AM</strong> local (<code>0 2 * * *</code>).</li>
    <li><strong>Política de Reintentos:</strong> 3 reintentos automáticos con intervalo de <strong>Backoff Exponencial</strong>.</li>
    <li><strong>Alertas y Notificaciones:</strong> Correos automatizados ante fallo de tarea (<code>on_failure_callback</code>) y reporte consolidado diario ante éxito.</li>
</ul>

<hr>

<h2>🔐 6. Entregable Fase 5: Gobierno, Seguridad y Calidad de Datos</h2>

<h3>6.1 Matriz de Roles y Accesos (RBAC)</h3>
<table border="1" cellspacing="0" cellpadding="5">
    <thead>
        <tr>
            <th>Rol</th>
            <th>Permisos en Azure IAM / AD</th>
            <th>Capa Bronze</th>
            <th>Capa Silver</th>
            <th>Capa Gold</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Data Engineer</strong></td>
            <td>Contributor + Storage Blob Data Contributor</td>
            <td>Lectura / Escritura</td>
            <td>Lectura / Escritura</td>
            <td>Lectura / Escritura</td>
        </tr>
        <tr>
            <td><strong>Data Analyst</strong></td>
            <td>Reader + Storage Blob Data Reader (Solo Gold)</td>
            <td>❌ Acceso Denegado</td>
            <td>❌ Acceso Denegado</td>
            <td>Lectura (Datos Anonimizados)</td>
        </tr>
        <tr>
            <td><strong>Administrator</strong></td>
            <td>Owner / User Access Administrator</td>
            <td>Control Total</td>
            <td>Control Total</td>
            <td>Control Total</td>
        </tr>
    </tbody>
</table>

<h3>6.2 Catálogo de Datos Básico</h3>

<h4>Tabla: <code>dim_conductores</code> (Capa Gold)</h4>
<table border="1" cellspacing="0" cellpadding="5">
    <thead>
        <tr>
            <th>Campo</th>
            <th>Tipo</th>
            <th>Origen</th>
            <th>Sensible (PII)</th>
            <th>Descripción</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>cond_id</code></td>
            <td><code>INT</code></td>
            <td><code>OPE_CONDUCTORES</code></td>
            <td>No</td>
            <td>Identificador único del conductor.</td>
        </tr>
        <tr>
            <td><code>num_doc_hash</code></td>
            <td><code>STRING</code></td>
            <td><code>OPE_CONDUCTORES</code></td>
            <td><strong>Sí (Enmascarado)</strong></td>
            <td>Hash SHA-256 del número de documento original[cite: 1].</td>
        </tr>
        <tr>
            <td><code>tip_vehiculo</code></td>
            <td><code>STRING</code></td>
            <td><code>OPE_CONDUCTORES</code></td>
            <td>No</td>
            <td>Categoría estandarizada (Moto, Bicicleta, Van, Camión)[cite: 1].</td>
        </tr>
        <tr>
            <td><code>antiguedad_anos</code></td>
            <td><code>FLOAT</code></td>
            <td>Calculado</td>
            <td>No</td>
            <td>Antigüedad en años calculada a partir de <code>fec_ingreso</code>[cite: 1].</td>
        </tr>
    </tbody>
</table>

<h4>Tabla: <code>fact_desempeno_conductor</code> (Capa Gold)</h4>
<table border="1" cellspacing="0" cellpadding="5">
    <thead>
        <tr>
            <th>Campo</th>
            <th>Tipo</th>
            <th>Origen</th>
            <th>Sensible (PII)</th>
            <th>Descripción</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>cond_id</code></td>
            <td><code>INT</code></td>
            <td><code>OPE_CONDUCTORES</code></td>
            <td>No</td>
            <td>Identificador del conductor.</td>
        </tr>
        <tr>
            <td><code>fec_evaluacion</code></td>
            <td><code>DATE</code></td>
            <td><code>TMS_ENVIOS</code> / <code>GPS_RUTAS</code></td>
            <td>No</td>
            <td>Fecha de consolidación del desempeño.</td>
        </tr>
        <tr>
            <td><code>score_desempeno</code></td>
            <td><code>FLOAT</code></td>
            <td>Calculado</td>
            <td>No</td>
            <td>Score multidimensional ponderado (rango 0.0 - 1.0)[cite: 1].</td>
        </tr>
    </tbody>
</table>

</details>
