variable "location" {
  description = "Región de Azure para desplegar los recursos"
  type        = string
  default     = "eastus"
}

variable "environment" {
  description = "Entorno de trabajo (ej. dev, prod)"
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "Nombre base del proyecto para nombrar recursos"
  type        = string
  default     = "datanow"
}