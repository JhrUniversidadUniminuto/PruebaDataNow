param rgName string = 'PruebasDataNow'
param location string = 'eastus'
param storageAccountName string = 'datalakejulian'

resource rg 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: rgName
  location: location
}

resource storage 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: storageAccountName
  location: location
  resourceGroup: rg.name
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    isHnsEnabled: true // ADLS Gen2
  }
}

resource bronze 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  parent: storage
  name: 'default/bronze'
  properties: {}
}

resource silver 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  parent: storage
  name: 'default/silver'
  properties: {}
}

resource gold 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  parent: storage
  name: 'default/gold'
  properties: {}
}
