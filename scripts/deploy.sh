#!/bin/bash

# Create resource group
az group create --name billing-opt-rg --location eastus

# Create storage account
az storage account create --name billingarchive --resource-group billing-opt-rg --location eastus --sku Standard_LRS

# Create container
az storage container create --name archived-billing --account-name billingarchive
