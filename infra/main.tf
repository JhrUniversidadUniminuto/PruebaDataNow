# Obtener información del cliente actual de Azure
data "azurerm_client_config" "current" {}

# 1. Referencia al Resource Group existente en tu cuenta
data "azurerm_resource_group" "rg" {
  name = "PruebasDataNow"
}

# 2. Storage Account con ADLS Gen2 (Creará el Storage dentro de PruebasDataNow)
# NOTA: En Azure los nombres de Storage Account deben ser globales, solo letras minúsculas y números (máx 24 caracteres).
resource "azurerm_storage_account" "adls" {
  name                     = "st${lower(replace(var.project_name, "/[^a-zA-Z0-9]/", ""))}${var.environment}"
  resource_group_name      = data.azurerm_resource_group.rg.name
  location                 = data.azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "StorageV2"
  is_hns_enabled           = true # ADLS Gen2 activado

  tags = data.azurerm_resource_group.rg.tags
}

# Contenedores Bronze, Silver y Gold
resource "azurerm_storage_container" "bronze" {
  name                  = "bronze"
  storage_account_name  = azurerm_storage_account.adls.name
  container_access_type = "private"
}

resource "azurerm_storage_container" "silver" {
  name                  = "silver"
  storage_account_name  = azurerm_storage_account.adls.name
  container_access_type = "private"
}

resource "azurerm_storage_container" "gold" {
  name                  = "gold"
  storage_account_name  = azurerm_storage_account.adls.name
  container_access_type = "private"
}

# 3. Azure Data Factory
resource "azurerm_data_factory" "adf" {
  name                = "adf-${lower(var.project_name)}-${var.environment}"
  location            = data.azurerm_resource_group.rg.location
  resource_group_name = data.azurerm_resource_group.rg.name

  tags = data.azurerm_resource_group.rg.tags
}

# 4. Log Analytics Workspace
resource "azurerm_log_analytics_workspace" "log_analytics" {
  name                = "log-${lower(var.project_name)}-${var.environment}"
  location            = data.azurerm_resource_group.rg.location
  resource_group_name = data.azurerm_resource_group.rg.name
  sku                 = "PerGB2018"
  retention_in_days   = 30

  tags = data.azurerm_resource_group.rg.tags
}

# 5. Action Group para Alertas
resource "azurerm_monitor_action_group" "action_group" {
  name                = "ag-${lower(var.project_name)}-${var.environment}"
  resource_group_name = data.azurerm_resource_group.rg.name
  short_name          = "data-alerts"

  email_receiver {
    name                    = "AdminEmail"
    email_address           = "admin@example.com" # Cambiar por tu correo
    use_common_alert_schema = true
  }

  tags = data.azurerm_resource_group.rg.tags
}

# 6. Azure Key Vault (Gestor de Secretos)
resource "azurerm_key_vault" "kv" {
  name                        = "kv-${lower(var.project_name)}-${var.environment}"
  location                    = data.azurerm_resource_group.rg.location
  resource_group_name         = data.azurerm_resource_group.rg.name
  enabled_for_disk_encryption = true
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  soft_delete_retention_days  = 7
  purge_protection_enabled    = false
  sku_name                    = "standard"

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id

    secret_permissions = [
      "Get", "List", "Set", "Delete", "Purge", "Recover"
    ]
  }

  tags = data.azurerm_resource_group.rg.tags
}