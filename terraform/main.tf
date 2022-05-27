resource "google_container_registry" "registry" {
    location = var.storage_location

    depends_on = [google_project_service.containerregistry]
}

resource "google_storage_bucket_iam_member" "viewer" {
    bucket = google_container_registry.registry.id
    role = "roles/storage.objectViewer"
    member = "allUsers"
}