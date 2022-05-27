variable "project_id" {}
variable "region" {
    default = "asia-northeast1"
}

terraform {
    required_version = "~> 1.1.9"

    required_providers {
        google = {
            source = "hashicorp/google"
            version = "4.22.0"
        }
    }
}

provider "google" {
    project = var.project_id
    region = var.region
}

data "google_project" "project" {
    project_id = var.project_id
}