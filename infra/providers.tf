terraform {
  required_version = ">= 1.5.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }

  # Desactivado para no buscar rg-terraform-state
  # backend "azurerm" {
  #   resource_group_name  = "PruebasDataNow"
  #   storage_account_name = "<nombre-de-tu-storage-existente>"
  #   container_name       = "tfstate"
  #   key                  = "data-pipeline.dev.tfstate"
  # }
}

provider "azurerm" {
  features {
    key_vault {
      purge_soft_delete_on_destroy = true
    }
  }
}