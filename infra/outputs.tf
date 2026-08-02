output "resource_group_name" {
  value       = data.azurerm_resource_group.rg.name
  description = "Nombre del Resource Group"
}

output "storage_account_name" {
  value       = azurerm_storage_account.adls.name
  description = "Nombre de la Storage Account ADLS Gen2"
}

output "adls_primary_dfs_endpoint" {
  value       = azurerm_storage_account.adls.primary_dfs_endpoint
  description = "URL endpoint de Data Lake Storage Gen2"
}

output "data_factory_name" {
  value       = azurerm_data_factory.adf.name
  description = "Nombre de Azure Data Factory"
}

output "key_vault_uri" {
  value       = azurerm_key_vault.kv.vault_uri
  description = "URI de Azure Key Vault"
}

output "log_analytics_id" {
  value       = azurerm_log_analytics_workspace.log_analytics.id
  description = "ID del Log Analytics Workspace"
}