# Entregable Fase 2 — Infraestructura como Código (Azure)

## Justificación de la Herramienta
Se eligió **Terraform** por ser una herramienta estándar en la industria para Infraestructura como Código (IaC). Permite aprovisionar recursos en **Azure** de forma declarativa, modular y segura, manteniendo el control de estado remoto y facilitando la gestión de múltiples entornos (dev/prod).

## Requisitos
- Terraform CLI (v1.5.0+)
- Azure CLI (`az login` realizado previa ejecución)

## Pasos para el Despliegue

1. Abrir la consola en la carpeta `C:\DataNow\infra`:
   ```bash
   cd C:\DataNow\infra