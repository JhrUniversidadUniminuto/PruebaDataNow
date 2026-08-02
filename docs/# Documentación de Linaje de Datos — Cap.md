# Documentación de Linaje de Datos — Capa Gold

En este documento se describe el linaje de 3 campos calculados clave presentes en las tablas de la capa Gold.

---

### 1. Campo: `total_spent`
* **Tabla de Origen**: `Silver.transactions`
* **Transformación Aplicada**: `SUM(amount)` agrupado por `customer_id` y `segment`.
* **Propósito**: Mide el valor acumulado total de ventas generadas por un cliente a lo largo de su ciclo de vida.
* **Fórmula / Lógica**:
  ```sql
  SUM(transactions.amount) GROUP BY customer_id